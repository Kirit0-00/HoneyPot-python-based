import json
import logging
from flask import Flask, render_template, request, jsonify, abort
from multiprocessing import Process
import sys
import os
import requests

# Add parent directory to path to import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import Config
from core.models import ConnectionEvent
from core.utils import get_timestamp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("web_server")

# Cache for geolocation to avoid redundant API calls
geo_cache = {}

def get_ip_info(ip):
    """Fetches geolocation info for an IP address."""
    if ip in ['127.0.0.1', 'localhost', '::1']:
        return {"country": "Local", "city": "Internal", "org": "Private Network"}
    
    if ip in geo_cache:
        return geo_cache[ip]
    
    try:
        # Using ip-api.com (free for non-commercial use)
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,org", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                geo_cache[ip] = data
                return data
    except Exception as e:
        logger.error(f"Geo lookup failed for {ip}: {e}")
    
    return {"country": "Unknown", "city": "Unknown", "org": "Unknown"}

def log_event(ip, port, data):
    """Logs a connection event to the central log file."""
    log_path = Config.LOG_PATH
    event = ConnectionEvent(
        timestamp=get_timestamp(),
        ip=ip,
        port=port,
        data=data
    )
    
    events = []
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                content = f.read().strip()
                if content:
                    events = json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
        
    events.append(event.to_dict())
    
    with open(log_path, 'w') as f:
        json.dump(events, f, indent=4)
    
    logger.info(f"Event logged from {ip} on port {port}")

# --- Decoy App ---
decoy_app = Flask(__name__, template_folder='templates')

@decoy_app.route('/')
def index():
    # Log the visit
    log_event(request.remote_addr, 8080, f"Visited Decoy Index - User-Agent: {request.user_agent}")
    return render_template('decoy.html')

@decoy_app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # Log the login attempt with credentials (captured!)
    log_event(request.remote_addr, 8080, f"Login Attempt - Username: {username}, Password: {password}")
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

# --- Dashboard App ---
dashboard_app = Flask(__name__, template_folder='templates')

def get_stats(events):
    total_events = len(events)
    unique_ips = len(set(e.get('ip') for e in events))
    
    ports = [e.get('port') for e in events]
    top_port = max(set(ports), key=ports.count) if ports else "N/A"
    
    port_counts = {}
    for p in set(ports):
        port_counts[str(p)] = ports.count(p)
    
    ips = [e.get('ip') for e in events]
    top_attackers = {}
    for ip in set(ips):
        top_attackers[ip] = {
            "count": ips.count(ip),
            "info": get_ip_info(ip)
        }
    
    # Sort top attackers and keep top 10
    top_attackers = dict(sorted(top_attackers.items(), key=lambda item: item[1]['count'], reverse=True)[:10])
    
    return {
        "total_events": total_events,
        "unique_ips": unique_ips,
        "top_port": top_port,
        "port_counts": port_counts,
        "top_attackers": top_attackers
    }

@dashboard_app.route('/')
def dashboard():
    # Security check: Only allow local access
    if request.remote_addr not in ['127.0.0.1', 'localhost', '::1']:
         logger.warning(f"Unauthorized access attempt to dashboard from {request.remote_addr}")
         abort(403)

    events = []
    try:
        if os.path.exists(Config.LOG_PATH):
            with open(Config.LOG_PATH, 'r') as f:
                content = f.read().strip()
                if content:
                    events = json.loads(content)
    except Exception as e:
        logger.error(f"Error loading logs: {e}")

    # Process geolocation for all events to display in table
    for event in events:
        if 'geo' not in event:
            event['geo'] = get_ip_info(event.get('ip'))

    stats = get_stats(events)
    return render_template('dashboard.html', events=events, stats=stats)

def run_decoy():
    logger.info("Starting Decoy Frontend on port 8080...")
    decoy_app.run(host='0.0.0.0', port=8080)

def run_dashboard():
    logger.info("Starting Dashboard on port 5000 (Local access only)...")
    dashboard_app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    p1 = Process(target=run_decoy)
    p2 = Process(target=run_dashboard)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
