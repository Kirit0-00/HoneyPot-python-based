import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration class for the Honeypot project."""
    
    # API Keys
    ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Ports to listen on
    # Expected format in .env: HONEYPOT_PORTS=21,22,80,443
    _ports_env = os.getenv("HONEYPOT_PORTS", "21,22,80,8080")
    HONEYPOT_PORTS = [int(p.strip()) for p in _ports_env.split(",") if p.strip().isdigit()]
    
    # Paths
    LOG_PATH = os.getenv("LOG_PATH", "logs/traffic.json")
    REPORT_PATH = os.getenv("REPORT_PATH", "reports/report.txt")
    AI_REPORT_PATH = os.getenv("AI_REPORT_PATH", "reports/ai_report.txt")
