# Phishing Email Detector

Analyzes a raw email (`.eml`) for common phishing indicators and assigns a risk
score.

## What it does
- Compares the From domain against the Return-Path / Reply-To domain (spoofing)
- Reads Authentication-Results for SPF / DKIM / DMARC failures
- Flags urgency / pressure language in the subject and body
- Detects URL shorteners, raw-IP links, and mismatched display-vs-actual links

## Requirements
- Python 3.8+ (standard library only)

## Usage
```
python phishing_detector.py suspicious.eml
```

Save an email as `.eml` (most clients offer "Save as" / "Show original") and
point the tool at it.
