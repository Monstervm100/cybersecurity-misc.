# File Integrity Monitor

Detects unauthorized changes to a directory by comparing SHA-256 hashes against
a saved baseline.

## What it does
- `baseline` mode: snapshots every file's SHA-256 hash, size, and mtime into
  `baseline.json`
- `check` mode: re-scans and reports files that were added, removed, or modified

## Requirements
- Python 3.8+ (standard library only)

## Usage
```
python fim.py baseline C:\path\to\watch
python fim.py check C:\path\to\watch
```

The baseline is stored as `baseline.json` in the current directory.
