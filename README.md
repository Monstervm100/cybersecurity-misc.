# Small Cybersecurity Projects

A collection of small educational cybersecurity demos and tools.

## Projects

### Caesar Cipher (`caesar-cipher/`)
An interactive browser-based Caesar Cipher tool. Open `caesar-cipher.html` directly in any browser — no setup needed.
- Encrypt and decrypt messages with a configurable shift (1–25)
- Live alphabet mapping preview (click to reveal)
- Copy-to-clipboard support

### Keylogger Demo (`keylogger/`)
Educational Python demos showing how keyboard and input capture works at the OS/framework level.

- **`keylogger_demo.py`** — Demonstrates tkinter keyboard event binding (`<KeyPress>` / `<KeyRelease>`). Only captures keys while the window is focused.
- **`input_capture_demo.py`** — Two-panel demo showing how `StringVar` traces in tkinter mirror input in real time.

**Requirements:** Python 3.x (tkinter is included with standard Python on Windows)

```
python keylogger_demo.py
python input_capture_demo.py
```

### AI Vulnerability Scanner (`ai-vulnerability-scanner/`)
An AI-powered pen-testing **assistant** (recon + assessment only). Takes a
target URL, enumerates subdomains (crt.sh), scans ports/services with nmap, and
uses Claude to identify likely vulnerabilities and remediation. See the folder
README for setup and the authorization requirements. **Authorized targets only.**

## Additional Tools (stubs — implementation pending)

Each folder contains a README describing the planned tool:

- `password-strength-checker/` — password strength & breach-list scoring
- `port-scanner/` — TCP/UDP port scanner with service fingerprinting
- `dns-whois-lookup/` — DNS record & WHOIS lookup tool
- `file-integrity-monitor/` — hash-based file change detection
- `log-analyzer/` — security-event log parsing & anomaly detection
- `packet-sniffer/` — live network traffic capture & inspection
- `vulnerability-scanner/` — known-CVE & misconfiguration checks
- `threat-intelligence-dashboard/` — IOC aggregation & enrichment
- `phishing-email-detector/` — email phishing-indicator analysis
- `ssh-honeypot/` — low-interaction SSH honeypot & attempt logging
- `siem-dashboard/` — lightweight SIEM event correlation dashboard

> ⚠️ The security/offensive tools in this repo are for **authorized testing and
> education only**. Only use them against systems you own or have explicit
> written permission to test.
