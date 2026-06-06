# Password Strength Checker

Evaluates a password's strength and checks whether it has appeared in known
public breaches.

## What it does
- Calculates entropy (bits) from length and character-set size
- Flags weak patterns: common passwords, sequences, keyboard walks, repeats, years
- Checks the password against the HaveIBeenPwned breach corpus using the
  k-anonymity API (only the first 5 chars of the SHA-1 hash leave your machine —
  the full password is never sent)
- Gives a rating (CRITICAL / WEAK / FAIR / STRONG / EXCELLENT) and suggestions

## Requirements
- Python 3.8+
- Internet access for the breach check (optional — it degrades gracefully)

## Usage
```
python password_checker.py
```
Input is hidden as you type.
