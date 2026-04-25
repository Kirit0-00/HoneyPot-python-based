import requests
import logging
import json
from typing import List
from core.models import ConnectionEvent
from core.config import Config
from core.utils import validate_ip

logger = logging.getLogger(__name__)

class IPEnricher:
    def __init__(self):
        self.api_key = Config.ABUSEIPDB_API_KEY
        self.url = "https://api.abuseipdb.com/api/v2/check"
        self.cache = {}

    def _assign_severity(self, score: int) -> str:
        if score > 80:
            return "Critical"
        elif score > 50:
            return "High"
        elif score > 20:
            return "Medium"
        return "Low"

    def check_ip(self, ip: str) -> dict:
        if not self.api_key or self.api_key == "your_abuseipdb_api_key_here":
            logger.warning("AbuseIPDB API key not configured. Skipping external request.")
            return {"abuseConfidenceScore": 0, "countryCode": "Unknown"}
            
        if not validate_ip(ip):
            return {"abuseConfidenceScore": 0, "countryCode": "Invalid"}

        if ip in self.cache:
            return self.cache[ip]

        headers = {
            'Accept': 'application/json',
            'Key': self.api_key
        }
        params = {
            'ipAddress': ip,
            'maxAgeInDays': '90'
        }

        try:
            response = requests.get(url=self.url, headers=headers, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json().get('data', {})
                self.cache[ip] = data
                return data
            elif response.status_code == 429:
                logger.warning("AbuseIPDB API rate limit exceeded.")
            else:
                logger.error(f"AbuseIPDB API Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to query AbuseIPDB for {ip}: {e}")

        return {"abuseConfidenceScore": 0, "countryCode": "Unknown"}

    def enrich_logs(self, log_path=None):
        log_path = log_path or Config.LOG_PATH
        try:
            with open(log_path, 'r') as f:
                data = json.load(f)
            
            enriched_events = []
            for item in data:
                event = ConnectionEvent.from_dict(item)
                
                # Check if already enriched
                if event.reputation_score is None:
                    intel = self.check_ip(event.ip)
                    score = intel.get('abuseConfidenceScore', 0)
                    event.reputation_score = score
                    event.severity = self._assign_severity(score)
                
                enriched_events.append(event.to_dict())

            with open(log_path, 'w') as f:
                json.dump(enriched_events, f, indent=4)
                
            logger.info("Logs enriched successfully.")
            
        except FileNotFoundError:
            logger.error(f"Log file not found for enrichment: {log_path}")
        except json.JSONDecodeError:
            logger.error(f"Failed to parse log file: {log_path}")
