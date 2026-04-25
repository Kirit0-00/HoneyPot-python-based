import os
import logging
from core.config import Config
from core.utils import ensure_directory_exists

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)

class AIAnalyst:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        if genai and self.api_key and self.api_key != "your_gemini_api_key_here":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.enabled = True
        else:
            self.enabled = False
            logger.warning("Gemini AI analyst is disabled. Check API key and google-generativeai package.")

    def _build_prompt(self, report_content: str) -> str:
        return f"""
You are a senior cybersecurity threat intelligence analyst specializing in network security and honeypot analysis. Analyze the following honeypot connection report and provide a structured, professional assessment.

**Report Content:**
{report_content}

**Analysis Requirements:**
Please structure your response with the following sections:

1. **Executive Summary**: Provide a concise overview of the threat activity observed, including total events, time period covered, and overall threat level (Low/Medium/High/Critical).

2. **Attack Patterns Identification**: Identify specific attack patterns or techniques used by attackers. Include:
   - Common ports targeted and their potential purposes (e.g., SSH brute force on port 22, HTTP scans on 80/8080, FTP exploits on 21).
   - Frequency and timing patterns (e.g., spikes in activity, distributed attacks).
   - Payload analysis if any data is captured.

3. **Threat Actor Profiling**: Based on IP addresses, enriched data, and behaviors:
   - Classify attackers (e.g., script kiddies, automated bots, targeted attackers).
   - Geographic distribution and potential origins.
   - Sophistication level and motivations.

4. **Risk Assessment**: Evaluate the potential impact if this were a real system:
   - Vulnerability exploitation potential.
   - Data exposure risks.
   - Network security implications.

5. **Anomaly Detection**: Highlight any unusual or concerning patterns not covered above, such as:
   - Zero-day attempts.
   - Rare port targeting.
   - High-frequency attacks from single IPs.

6. **Recommendations**:
   - Immediate mitigation steps for similar real systems.
   - Long-term security improvements (e.g., firewall rules, intrusion detection).
   - Monitoring and alerting enhancements.

Be precise, evidence-based, and focus on actionable intelligence. If data is insufficient for any section, note it clearly.
"""

    def analyze_report(self, report_path=None, output_path=None):
        if not self.enabled:
            logger.error("AI Analyst is not enabled. Cannot run analysis.")
            return

        report_path = report_path or Config.REPORT_PATH
        output_path = output_path or Config.AI_REPORT_PATH
        
        try:
            with open(report_path, 'r') as f:
                report_content = f.read()
                
            prompt = self._build_prompt(report_content)
            logger.info("Sending report to AI for analysis...")
            
            response = self.model.generate_content(prompt)
            ai_analysis = response.text
            
            ensure_directory_exists(output_path)
            with open(output_path, 'w') as f:
                f.write("=== AI Threat Analysis ===\n\n")
                f.write(ai_analysis)
                
            logger.info(f"AI analysis saved to {output_path}")
            
        except FileNotFoundError:
            logger.error(f"Standard report not found at {report_path}. Run regular analysis first.")
        except Exception as e:
            logger.error(f"AI Analysis failed: {e}")
