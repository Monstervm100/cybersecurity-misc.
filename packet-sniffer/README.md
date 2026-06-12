# Packet Sniffer

Captures live network traffic and summarises it by protocol and conversation.

## ⚠️ Authorization
Only capture traffic on networks you own or are explicitly authorized to monitor.
Capturing requires administrator / root privileges.

## What it does
- Live capture via scapy with an optional BPF filter
- Per-packet line: source/destination, protocol, ports, TCP flags, DNS queries
- Running summary: packet counts by protocol and top talker pairs

## Requirements
- Python 3.8+
- `pip install -r requirements.txt` (scapy)
- On Windows, install Npcap (https://npcap.com) for capture support
- Run as administrator / with sudo

## Usage
```
python packet_sniffer.py
python packet_sniffer.py --count 200 --filter "tcp port 443"
python packet_sniffer.py --iface "Wi-Fi"
```
