# DNS & WHOIS Lookup Tool

Resolves DNS information and queries WHOIS registration data for a domain.

## What it does
- Resolves A records, canonical name, and aliases
- Performs reverse (PTR) lookups for each IP
- Queries the appropriate WHOIS server (port 43) and shows the key fields:
  registrar, creation/expiry dates, name servers, status, registrant

## Requirements
- Python 3.8+ (standard library only)

## Usage
```
python dns_whois.py example.com
python dns_whois.py example.com --no-whois
```

Note: WHOIS server coverage is handled for common TLDs; others fall back to IANA.
