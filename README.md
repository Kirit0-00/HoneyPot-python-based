# Modular Python Honeypot System

A sophisticated honeypot system written in Python that captures and analyzes network traffic to detect potential security threats. The system provides threat intelligence enrichment, a professional web decoy, a private analytics dashboard, and AI-powered analysis capabilities.

## Features

- **Multi-Port Listening**: Simultaneously monitor multiple network ports (FTP, SSH, HTTP, etc.)
- **Web Decoy**: A "legit" looking corporate login page to attract and capture web-based attacks.
- **Analytics Dashboard**: A premium, private dashboard for real-time monitoring of attack patterns.
- **Connection Logging**: Capture and store detailed connection events, including captured credentials from the decoy.
- **Threat Intelligence**: Enrich captured data with AbuseIPDB threat intelligence.
- **AI Analysis**: Generate intelligent reports using Google's Gemini AI.
- **Modular Architecture**: Clean separation of concerns across different components.

## Project Structure

```
Honey_Pot_project/
├── main.py                 # Main entry point with CLI interface
├── requirements.txt         # Python dependencies
├── core/                   # Core utilities and models
│   ├── config.py           # Configuration management
│   ├── models.py           # Data models (ConnectionEvent, Report)
│   └── utils.py            # Helper functions
├── trap/                   # Honeypot implementation
│   └── honeypot.py         # Main socket server logic
├── web/                    # Web-based honeypot features
│   ├── server.py           # Flask server for Decoy and Dashboard
│   └── templates/          # HTML templates (Decoy & Dashboard)
├── analysis/               # Log analysis and reporting
│   └── analyzer.py         # Log analysis logic
├── intel/                  # Threat intelligence integration
│   ├── enricher.py         # AbuseIPDB integration
│   └── ai_analyst.py       # Gemini AI analysis
├── logs/                   # Captured traffic logs (JSON)
└── reports/                # Generated text and AI reports
```

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   Create a `.env` file in the project root:
   ```env
   ABUSEIPDB_API_KEY=your_key
   GEMINI_API_KEY=your_key
   HONEYPOT_PORTS=21,22,80,8080
   LOG_PATH=logs/traffic.json
   ```

## Usage

The honeypot provides several command-line options:

### 1. Start the Full System (Web + Sockets)
```bash
python main.py --start --web
```
This starts:
- **Socket Listener**: Monitors ports like 21 (FTP) and 22 (SSH).
- **Web Decoy**: A fake login portal at `http://localhost:8080`.
- **Private Dashboard**: Accessible only at `http://localhost:5000`.

### 2. Start Only Web Services
```bash
python main.py --web
```

### 3. Analyze and Enrich Logs
```bash
python main.py --enrich   # Add threat intel
python main.py --analyze  # Generate basic report
python main.py --ai       # Generate AI-powered insights
```

## Accessing the Dashboard

The analytics dashboard is designed for **your eyes only**. 
- It binds to `127.0.0.1` and blocks external IP addresses by default.
- Access it locally at: **`http://localhost:5000`**

## Security Considerations

- **Isolation**: Always run the honeypot in a controlled or isolated environment.
- **Dashboard Privacy**: The dashboard is restricted to local access by default to prevent attackers from seeing your logs.
- **Decoy Realism**: The web decoy is hosted on port 8080 by default. For a more "legit" look, you can map port 80 to 8080 using `iptables` or run as root (not recommended for research).

## License

This project is provided for educational and security research purposes. Deployment should comply with local laws and regulations.
