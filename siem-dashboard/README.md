# SIEM Dashboard

A self-contained browser dashboard that displays and correlates security events,
in the style of a lightweight Security Information and Event Management console.

## What it does
- Shows a timeline of security events with timestamp, source, severity, and message
- Live search and severity filtering
- Summary cards counting events by severity
- "Simulate event" button to push a new event onto the stream (demo)

## Usage
Double-click `index.html` to open it in any browser — no setup, no server.

## Customising
The `TYPES` array near the bottom of `index.html` defines the event templates.
Replace it (or wire the page to a real log/alert source) to feed live events
instead of the sample stream.
