import argparse
import logging
import sys

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
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    try:
        if args.start:
            logger.info("Initializing Honeypot...")
            server = HoneypotServer()
            server.start()

        if args.enrich:
            logger.info("Enriching logs with threat intelligence...")
            enricher = IPEnricher()
            enricher.enrich_logs()
            
        if args.analyze:
            logger.info("Analyzing logs and generating report...")
            analyzer = LogAnalyzer()
            analyzer.generate_report()
            
        if args.ai:
            logger.info("Running AI Analyst...")
            ai = AIAnalyst()
            ai.analyze_report()
            
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
