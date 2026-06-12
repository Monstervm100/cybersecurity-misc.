import argparse
import sys
from collections import Counter

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, DNS
except ImportError:
    print("scapy is required. Install with: pip install scapy")
    sys.exit(1)

PROTO = {6: "TCP", 17: "UDP", 1: "ICMP"}
stats = Counter()
talkers = Counter()


def describe(pkt):
    if IP not in pkt:
        return None
    ip = pkt[IP]
    proto = PROTO.get(ip.proto, str(ip.proto))
    stats[proto] += 1
    talkers[(ip.src, ip.dst)] += 1

    line = f"{ip.src:>15} -> {ip.dst:<15} {proto}"
    if TCP in pkt:
        line += f" {pkt[TCP].sport}->{pkt[TCP].dport} [{pkt[TCP].flags}]"
    elif UDP in pkt:
        line += f" {pkt[UDP].sport}->{pkt[UDP].dport}"
        if DNS in pkt and pkt[DNS].qd is not None:
            try:
                line += f" DNS? {pkt[DNS].qd.qname.decode(errors='replace')}"
            except Exception:
                pass
    elif ICMP in pkt:
        line += f" type={pkt[ICMP].type}"
    return line


def main():
    parser = argparse.ArgumentParser(description="Live packet sniffer (scapy).")
    parser.add_argument("--count", type=int, default=0, help="packets to capture (0 = until Ctrl+C)")
    parser.add_argument("--filter", default="", help="BPF filter, e.g. 'tcp port 80'")
    parser.add_argument("--iface", default=None, help="interface name (default: scapy picks)")
    args = parser.parse_args()

    print("=" * 60)
    print("  Only capture traffic on networks you own or are authorized")
    print("  to monitor. Capturing requires administrator privileges.")
    print("=" * 60)

    def cb(pkt):
        line = describe(pkt)
        if line:
            print(line)

    try:
        sniff(prn=cb, count=args.count, filter=args.filter or None, iface=args.iface, store=False)
    except PermissionError:
        print("Permission denied - run as administrator / root.")
        return
    except KeyboardInterrupt:
        pass

    print("\n--- Summary ---")
    for proto, n in stats.most_common():
        print(f"  {proto}: {n}")
    print("\nTop conversations:")
    for (src, dst), n in talkers.most_common(10):
        print(f"  {src} -> {dst}: {n}")


if __name__ == "__main__":
    main()
