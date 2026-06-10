# Log Analyzer

Parses a log file and surfaces security-relevant events: brute-force attempts,
error spikes, top source IPs, and HTTP status-code breakdowns.

## What it does
- Counts failed-auth lines per source IP and flags likely brute-force sources
- Tallies error/critical lines
- Ranks the busiest source IPs
- Summarises HTTP status codes (highlighting 4xx/5xx) for web access logs

## Requirements
- Python 3.8+ (standard library only)

## Usage
```
python log_analyzer.py /var/log/auth.log
python log_analyzer.py access.log --threshold 10
```

Works with common formats (syslog/auth.log, web access logs) by pattern-matching
rather than assuming a fixed schema.
