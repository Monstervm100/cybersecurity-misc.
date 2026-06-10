import argparse
import re
import sys
from collections import Counter

IP_RE = re.compile(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b")
FAIL_RE = re.compile(r"(failed password|authentication failure|invalid user|login failed|access denied)", re.I)
ERROR_RE = re.compile(r"\b(error|critical|fatal|denied|unauthorized)\b", re.I)
HTTP_RE = re.compile(r'"\w+\s+\S+\s+HTTP/[\d.]+"\s+(\d{3})')


def analyze(path, threshold):
    fails_by_ip = Counter()
    ip_hits = Counter()
    status_codes = Counter()
    errors = 0
    lines = 0

    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"Cannot open {path}: {exc}")
        sys.exit(1)

    with fh:
        for line in fh:
            lines += 1
            ips = IP_RE.findall(line)
            for ip in ips:
                ip_hits[ip] += 1
            if FAIL_RE.search(line):
                for ip in ips:
                    fails_by_ip[ip] += 1
            if ERROR_RE.search(line):
                errors += 1
            m = HTTP_RE.search(line)
            if m:
                status_codes[m.group(1)] += 1

    print(f"\n--- Log Analysis: {path} ---")
    print(f"Lines processed : {lines}")
    print(f"Lines w/ errors : {errors}")

    brute = {ip: n for ip, n in fails_by_ip.items() if n >= threshold}
    print(f"\nPossible brute-force sources (>= {threshold} failed auths):")
    if brute:
        for ip, n in sorted(brute.items(), key=lambda x: -x[1]):
            print(f"  {ip:<16} {n} failed attempts")
    else:
        print("  none detected")

    print("\nTop source IPs:")
    for ip, n in ip_hits.most_common(10):
        print(f"  {ip:<16} {n} hits")

    if status_codes:
        print("\nHTTP status codes:")
        for code, n in sorted(status_codes.items()):
            flag = "  <-- review" if code.startswith(("4", "5")) else ""
            print(f"  {code}: {n}{flag}")


def main():
    parser = argparse.ArgumentParser(description="Security-focused log analyzer.")
    parser.add_argument("logfile", help="Path to a log file")
    parser.add_argument("--threshold", type=int, default=5,
                        help="failed-auth count that flags an IP (default 5)")
    args = parser.parse_args()
    analyze(args.logfile, args.threshold)


if __name__ == "__main__":
    main()
