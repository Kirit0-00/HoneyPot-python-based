# Modular Python Honeypot System

A sophisticated honeypot system written in Python that captures and analyzes network traffic to detect potential security threats. The system provides threat intelligence enrichment and AI-powered analysis capabilities.

## Features

- **Multi-Port Listening**: Simultaneously monitor multiple network ports (FTP, SSH, HTTP, etc.)
- **Connection Logging**: Capture and store detailed connection events with timestamps
- **Threat Intelligence**: Enrich captured data with AbuseIPDB threat intelligence
- **AI Analysis**: Generate intelligent reports using Google's Gemini AI
- **Modular Architecture**: Clean separation of concerns across different components
- **Environment Configuration**: Secure API key management with `.env` files

## Project Structure

```
Honey_Pot_project/
├── main.py                 # Main entry point with CLI interface
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore patterns
├── core/                   # Core utilities and models
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── models.py           # Data models (ConnectionEvent, Report)
│   └── utils.py            # Helper functions (IP validation, timestamps)
├── trap/                   # Honeypot implementation
│   ├── __init__.py
│   └── honeypot.py         # Main honeypot server logic
├── analysis/               # Log analysis and reporting
│   ├── __init__.py
│   └── analyzer.py         # Log analysis and report generation
├── intel/                  # Threat intelligence integration
│   ├── __init__.py
│   ├── enricher.py         # AbuseIPDB integration
│   └── ai_analyst.py       # Gemini AI analysis
└── logs/                   # Generated logs (created automatically)
    └── reports/            # Generated reports (created automatically)
```

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root with:
   ```env
   ABUSEIPDB_API_KEY=your_abuseipdb_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   HONEYPOT_PORTS=21,22,80,8080
   LOG_PATH=logs/traffic.json
   REPORT_PATH=reports/report.txt
   AI_REPORT_PATH=reports/ai_report.txt
   ```

## Usage

The honeypot provides several command-line options:

### Start the Honeypot Server
```bash
python main.py --start
```
Starts listening on configured ports and captures incoming connections.

### Analyze Captured Logs
```bash
python main.py --analyze
```
Processes logged events and generates a detailed analysis report.

### Enrich Logs with Threat Intelligence
```bash
python main.py --enrich
```
Queries AbuseIPDB for IP reputation data and enriches the logs.

### Generate AI Analysis
```bash
python main.py --ai
```
Uses Google's Gemini AI to analyze the threat patterns and provide intelligent insights.

### Show Help
```bash
python main.py
```
Displays all available options.

## Configuration

### Ports
Configure which ports to monitor in your `.env` file:
```
HONEYPOT_PORTS=21,22,80,443,8080
```

### File Paths
Customize log and report locations:
```
LOG_PATH=logs/traffic.json
REPORT_PATH=reports/report.txt
AI_REPORT_PATH=reports/ai_report.txt
```

## API Keys

### AbuseIPDB
1. Sign up at [AbuseIPDB](https://www.abuseipdb.com/)
2. Get your API key from the account settings
3. Add it to your `.env` file as `ABUSEIPDB_API_KEY`

### Google Gemini
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

## How It Works

1. **Honeypot Server**: Listens on multiple ports using multithreading
2. **Connection Handling**: Captures incoming connections and logs metadata
3. **Fake Responses**: Sends appropriate responses based on port (FTP banner, HTTP response, etc.)
4. **Log Storage**: Saves events to JSON format with timestamps and connection details
5. **Analysis**: Processes logs to identify patterns, top attackers, and targeted ports
6. **Threat Enrichment**: Queries external APIs for IP reputation and threat scores
7. **AI Analysis**: Uses machine learning to provide contextual threat analysis

## Security Considerations

- **Port Access**: Ensure the honeypot only listens on ports you intend to monitor
- **API Keys**: Keep API keys secure and never commit them to version control
- **Network Isolation**: Consider running in an isolated network environment
- **Logging**: Monitor log files for sensitive data exposure
- **Permissions**: Run with appropriate system permissions for port binding

## Contributing

1. Follow the modular architecture when adding new features
2. Add appropriate logging for debugging and monitoring
3. Update documentation for any new configuration options
4. Test thoroughly in isolated environments

## License

This project is provided as-is for educational and security research purposes. Please ensure compliance with applicable laws and regulations when deploying honeypots.

## Educational Resources

For a comprehensive guide to the Python concepts used in this project, see `python_curriculum_explanations.md` which covers:
- Python fundamentals (variables, data types, operators)
- Control flow and functions
- Object-oriented programming
- File operations and multithreading
- Real-world examples from this honeypot codebase
