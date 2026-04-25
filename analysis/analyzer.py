import json
import logging
from collections import Counter
from typing import List, Dict
from core.models import ConnectionEvent, Report
from core.config import Config
from core.utils import get_timestamp, ensure_directory_exists

logger = logging.getLogger(__name__)

class LogAnalyzer:
    def __init__(self, log_path=None):
        self.log_path = log_path or Config.LOG_PATH

    def load_logs(self) -> List[ConnectionEvent]:
        try:
            with open(self.log_path, 'r') as f:
                data = json.load(f)
                return [ConnectionEvent.from_dict(item) for item in data]
        except FileNotFoundError:
            logger.warning(f"Log file not found: {self.log_path}")
            return []
        except json.JSONDecodeError:
            logger.error(f"Failed to parse log file: {self.log_path}")
            return []

    def get_top_attackers(self, events: List[ConnectionEvent], top_n=5) -> Dict[str, int]:
        ips = [event.ip for event in events]
        return dict(Counter(ips).most_common(top_n))

    def get_targeted_ports(self, events: List[ConnectionEvent]) -> Dict[int, int]:
        ports = [event.port for event in events]
        return dict(Counter(ports))

    def detect_patterns(self, events: List[ConnectionEvent]) -> Report:
        top_attackers = self.get_top_attackers(events)
        targeted_ports = self.get_targeted_ports(events)
        
        # High severity IPs can be determined if enriched logs exist
        high_severity = list(set([e.ip for e in events if getattr(e, 'severity', None) in ('High', 'Critical')]))
        
        return Report(
            generated_at=get_timestamp(),
            total_events=len(events),
            top_attackers=top_attackers,
            targeted_ports=targeted_ports,
            high_severity_ips=high_severity
        )
        
    def generate_report(self, output_path=None):
        output_path = output_path or Config.REPORT_PATH
        ensure_directory_exists(output_path)
        
        events = self.load_logs()
        if not events:
            logger.info("No logs to analyze.")
            return

        report = self.detect_patterns(events)
        
        with open(output_path, 'w') as f:
            f.write(f"Honeypot Analysis Report - {report.generated_at}\n")
            f.write("="*50 + "\n\n")
            f.write(f"Total Events: {report.total_events}\n\n")
            
            f.write("Top Attackers:\n")
            for ip, count in report.top_attackers.items():
                f.write(f"  - {ip}: {count} times\n")
                
            f.write("\nTargeted Ports:\n")
            for port, count in report.targeted_ports.items():
                f.write(f"  - Port {port}: {count} times\n")
                
            if report.high_severity_ips:
                f.write("\nHigh Severity IPs:\n")
                for ip in report.high_severity_ips:
                    f.write(f"  - {ip}\n")
                    
        logger.info(f"Report generated successfully at {output_path}")
