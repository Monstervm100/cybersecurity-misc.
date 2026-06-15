# Threat Intelligence Dashboard

A self-contained browser dashboard for browsing aggregated indicators of
compromise (IOCs).

## What it does
- Displays IOCs (IPs, domains, hashes, URLs) with threat, severity, source, and
  last-seen date
- Live search across indicator / threat / source
- Filter by type and severity
- Summary cards counting IOCs by severity

## Usage
Double-click `index.html` to open it in any browser — no setup, no server.

## Customising
The dataset is the `IOCS` array near the bottom of `index.html`. Replace the
sample entries with real feed data (AbuseIPDB, URLhaus, PhishTank, VirusTotal,
etc.) to use it for live triage.
