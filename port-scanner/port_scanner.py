import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_PORTS = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns",
    80: "http", 110: "pop3", 143: "imap", 443: "https", 445: "smb",
    993: "imaps", 995: "pop3s", 1433: "mssql", 3306: "mysql",
    3389: "rdp", 5432: "postgres", 5900: "vnc", 6379: "redis",
    8080: "http-alt", 8443: "https-alt", 27017: "mongodb",
}


def authorize(target):
    print("=" * 60)
    print("  AUTHORIZATION REQUIRED")
    print("=" * 60)
    print(f"You are about to port-scan: {target}")
    print("Only scan systems you own or have written permission to test.")
    answer = input(f'Type "{target}" to confirm authorization: ').strip()
    if answer != target:
        print("Confirmation failed. Aborting.")
        sys.exit(1)


def grab_banner(sock):
    try:
        sock.settimeout(1.5)
        data = sock.recv(128)
        return data.decode("utf-8", errors="replace").strip()
    except Exception:
        return ""


def scan_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((host, port)) == 0:
                return port, grab_banner(s)
    except Exception:
        pass
    return None


def main():
    parser = argparse.ArgumentParser(description="Threaded TCP connect port scanner.")
    parser.add_argument("target", help="Hostname or IP to scan")
    parser.add_argument("--ports", default="common",
                        help='"common", "1-1024", or comma list like "22,80,443"')
    parser.add_argument("--timeout", type=float, default=1.0)
    parser.add_argument("--threads", type=int, default=100)
    parser.add_argument("--yes", action="store_true", help="skip authorization prompt")
    args = parser.parse_args()

    try:
        host = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"Could not resolve {args.target}")
        sys.exit(1)

    if not args.yes:
        authorize(args.target)

    if args.ports == "common":
        ports = sorted(COMMON_PORTS)
    elif "-" in args.ports:
        a, b = args.ports.split("-")
        ports = range(int(a), int(b) + 1)
    else:
        ports = [int(p) for p in args.ports.split(",")]

    print(f"\nScanning {args.target} ({host}) ...\n")
    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = [ex.submit(scan_port, host, p, args.timeout) for p in ports]
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                open_ports.append(res)

    if not open_ports:
        print("No open ports found.")
        return
    for port, banner in sorted(open_ports):
        name = COMMON_PORTS.get(port, "unknown")
        line = f"  {port:>5}/tcp  open  {name}"
        if banner:
            line += f"  [{banner[:60]}]"
        print(line)
    print(f"\n{len(open_ports)} open port(s).")


if __name__ == "__main__":
    main()
