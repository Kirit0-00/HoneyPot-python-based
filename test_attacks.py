#!/usr/bin/env python3
"""
Test script to generate dummy attacks on the honeypot for demonstration purposes.
This simulates various types of connections to populate logs for analysis.
"""

import socket
import time
import threading
import random

def test_connection(ip, port, data=""):
    """Send a test connection to honeypot"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))
        if data:
            sock.send(data.encode())
        time.sleep(0.1)  # Brief pause to allow logging
        sock.close()
        print(f"✓ Connection to {ip}:{port} successful")
    except Exception as e:
        print(f"✗ Connection to {ip}:{port} failed: {e}")

def generate_test_attacks(target_ip="127.0.0.1", ports=[21, 22, 80, 8080], num_connections=5):
    """Generate multiple test connections across different ports"""

    print(f"Generating {num_connections} test connections per port to {target_ip}")
    print("Make sure honeypot is running with: python main.py --start")

    # Test data for different ports
    test_data = {
        21: "USER test\r\n",  # FTP
        22: "SSH-2.0-OpenSSH_8.0\r\n",  # SSH
        80: "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n",  # HTTP
        8080: "GET /test HTTP/1.1\r\nHost: localhost\r\n\r\n"  # HTTP alt
    }

    threads = []
    for port in ports:
        for i in range(num_connections):
            data = test_data.get(port, "")
            t = threading.Thread(target=test_connection, args=(target_ip, port, data))
            threads.append(t)
            t.start()
            time.sleep(0.1)  # Stagger connections

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("\nTest connections completed!")
    print("Run 'python main.py --analyze' to generate a report from captured logs")

def simulate_attacker_ips():
    """Generate connections from different simulated IP addresses using localhost"""
    print("Simulating connections from multiple 'attacker' IPs (using localhost)")

    # In a real scenario, you'd use different IPs, but for testing we use localhost
    fake_ips = ["127.0.0.1"] * 20  # Simulate multiple connections from same IP

    for ip in fake_ips:
        port = random.choice([21, 22, 80, 8080])
        test_connection(ip, port, f"Test attack data {random.randint(1,100)}")
        time.sleep(0.2)

if __name__ == "__main__":
    print("Honeypot Test Attack Generator")
    print("=" * 40)

    # Basic test
    generate_test_attacks()

    # Additional attacker simulation
    simulate_attacker_ips()

    print("\nNext steps:")
    print("1. Run: python main.py --analyze")
    print("2. Check reports/report.txt for analysis")
    print("3. Run: python main.py --enrich (if API keys configured)")
    print("4. Run: python main.py --ai (if Gemini API configured)")
