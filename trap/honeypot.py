import socket
import threading
import json
import logging
from core.models import ConnectionEvent
from core.utils import get_timestamp, ensure_directory_exists
from core.config import Config

logger = logging.getLogger(__name__)

class HoneypotServer:
    def __init__(self, ports=None):
        self.ports = ports or Config.HONEYPOT_PORTS
        self.log_path = Config.LOG_PATH
        self.threads = []
        self.interface = Config.INTERFACE_IP
        self.running = False
        ensure_directory_exists(self.log_path)

    def start(self):
        self.running = True
        logger.info(f"Starting honeypot on ports: {self.ports}")
        for port in self.ports:
            t = threading.Thread(target=self._listen, args=(self.interface,port,), daemon=True)
            self.threads.append(t)
            t.start()
            
        try:
            # Keep main thread alive
            for t in self.threads:
                t.join()
        except KeyboardInterrupt:
            logger.info("Shutting down honeypot servers...")
            self.stop()

    def stop(self):
        self.running = False

    def _listen(self,interface,port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((interface, port))
                s.listen(5)
                logger.info(f"Listening on interface {interface} port {port}...")
                
                s.settimeout(1.0) # Check self.running periodically
                while self.running:
                    try:
                        conn, addr = s.accept()
                        threading.Thread(target=self._handle_client, args=(conn, addr, port), daemon=True).start()
                    except socket.timeout:
                        continue
                    except Exception as e:
                        if self.running:
                            logger.error(f"Error on port {port}: {e}")
        except Exception as e:
            logger.error(f"Failed to bind to port {port}: {e}")

    def _handle_client(self, conn, addr, port):
        ip = addr[0]
        try:
            conn.settimeout(3.0)
            data = conn.recv(1024).decode('utf-8', errors='ignore').strip()
            
            event = ConnectionEvent(
                timestamp=get_timestamp(),
                ip=ip,
                port=port,
                data=data
            )
            
            self._log_event(event)
            logger.info(f"Connection captured from {ip}:{port}")
            
            # Send fake response based on port
            self._send_fake_response(conn, port)
        except socket.timeout:
            event = ConnectionEvent(timestamp=get_timestamp(), ip=ip, port=port, data="<Timeout>")
            self._log_event(event)
            logger.info(f"Connection captured from {ip}:{port} (Timeout)")
        except Exception as e:
            logger.error(f"Error handling client {ip}: {e}")
        finally:
            conn.close()

    def _log_event(self, event: ConnectionEvent):
        events = []
        try:
            with open(self.log_path, 'r') as f:
                content = f.read().strip()
                if content:
                    events = json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
            
        events.append(event.to_dict())
        
        with open(self.log_path, 'w') as f:
            json.dump(events, f, indent=4)

    def _send_fake_response(self, conn, port):
        if port == 22:
            conn.sendall(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n")
        elif port in [80, 8080]:
            response = "HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\nContent-Length: 0\r\n\r\n"
            conn.sendall(response.encode('utf-8'))
        elif port == 21:
            conn.sendall(b"220 (vsFTPd 3.0.3)\r\n")
