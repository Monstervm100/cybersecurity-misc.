# SSH Honeypot

A low-interaction SSH honeypot that presents a realistic SSH banner and logs
every connection attempt. It grants no shell and no access to any real system —
it only captures who is knocking.

## ⚠️ Authorization
Deploy only on infrastructure you own. The honeypot is designed to attract and
log attacks against *itself*; it exposes nothing real.

## What it does
- Listens on a port (default 2222) and sends a believable SSH server banner
- Logs the source IP, port, and the client's identification string
- Writes timestamped entries to `honeypot.log` and to the console
- Handles many simultaneous connections (one thread each)

## Requirements
- Python 3.8+ (standard library only)

## Usage
```
python ssh_honeypot.py
python ssh_honeypot.py --port 22       (requires elevated privileges)
python ssh_honeypot.py --host 0.0.0.0 --port 2222
```

Logs are appended to `honeypot.log` in the current directory.
