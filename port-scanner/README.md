# Port Scanner

A threaded TCP connect-scan tool that finds open ports and grabs service banners.

## ⚠️ Authorization
Only scan hosts you own or have explicit written permission to test.
Unauthorized port scanning is illegal in most jurisdictions. The tool requires
you to type the target name to confirm authorization (bypass with `--yes` only
for pre-authorized use).

## What it does
- Resolves the target and scans ports concurrently (TCP connect)
- Identifies common services by port number
- Grabs a short service banner where one is offered

## Requirements
- Python 3.8+ (standard library only)

## Usage
```
python port_scanner.py example.com
python port_scanner.py 192.168.1.10 --ports 1-1024
python port_scanner.py example.com --ports 22,80,443 --threads 200
```
