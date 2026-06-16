# SSH Honeypot

A low-interaction SSH honeypot that logs intrusion attempts.

## Planned Features
- Fake SSH banner and auth prompt (no real shell access)
- Logging of source IPs, usernames, and attempted passwords
- Geolocation enrichment of attacker IPs
- Stats and reporting on attack patterns

## Authorization
Deploy only on infrastructure you own. Designed to capture attacks against
itself — it grants no access to any real system.

## Status
Stub — implementation pending.
