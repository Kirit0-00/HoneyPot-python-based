import argparse
import logging
import sys
import os

from core.config import Config
from trap.honeypot import HoneypotServer
from analysis.analyzer import LogAnalyzer
from intel.enricher import IPEnricher
from intel.ai_analyst import AIAnalyst

# Configure main logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
)
logger = logging.getLogger("main")

def main():
    parser = argparse.ArgumentParser(description="Modular Python Honeypot System")
    parser.add_argument('--start', action='store_true', help='Start the honeypot listener')
    parser.add_argument('--analyze', action='store_true', help='Analyze captured logs and generate a report')
    parser.add_argument('--enrich', action='store_true', help='Enrich logs with Threat Intel (AbuseIPDB)')
    parser.add_argument('--ai', action='store_true', help='Generate AI analysis based on the report')
    parser.add_argument('--web', action='store_true', help='Start the web decoy and dashboard')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    try:
        processes = []

        if args.web:
            logger.info("Starting Web Decoy and Dashboard...")
            from web.server import run_decoy, run_dashboard
            from multiprocessing import Process
            p_decoy = Process(target=run_decoy, daemon=True)
            p_dash = Process(target=run_dashboard, daemon=True)
            p_decoy.start()
            p_dash.start()
            processes.extend([p_decoy, p_dash])

        if args.start:
            logger.info("Initializing Honeypot Socket Server...")
            ports = Config.HONEYPOT_PORTS
            if args.web and 8080 in ports:
                ports = [p for p in ports if p != 8080]
                logger.info(f"Excluding port 8080 from socket server (managed by Web Decoy). Ports: {ports}")
            
            server = HoneypotServer(ports=ports)
            if args.web:
                from multiprocessing import Process
                p_socket = Process(target=server.start, daemon=True)
                p_socket.start()
                processes.append(p_socket)
            else:
                server.start()

        if args.enrich:
            logger.info("Enriching logs...")
            IPEnricher().enrich_logs()
            
        if args.analyze:
            logger.info("Generating report...")
            LogAnalyzer().generate_report()
            
        if args.ai:
            logger.info("Running AI Analyst...")
            AIAnalyst().analyze_report()

        if processes:
            try:
                for p in processes:
                    p.join()
            except KeyboardInterrupt:
                logger.info("Shutting down background services...")
                for p in processes:
                    p.terminate()

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
