import argparse
import socket
import sys

WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com",
    "net": "whois.verisign-grs.com",
    "org": "whois.pir.org",
    "io": "whois.nic.io",
    "co": "whois.nic.co",
    "info": "whois.afilias.net",
    "dev": "whois.nic.google",
    "app": "whois.nic.google",
}


def dns_records(domain):
    print(f"\n--- DNS for {domain} ---")
    try:
        name, aliases, addrs = socket.gethostbyname_ex(domain)
        print(f"Canonical name : {name}")
        if aliases:
            print(f"Aliases        : {', '.join(aliases)}")
        print(f"A records      : {', '.join(addrs)}")
        for ip in addrs:
            try:
                rev = socket.gethostbyaddr(ip)[0]
                print(f"  {ip} -> {rev}")
            except socket.herror:
                print(f"  {ip} -> (no PTR)")
    except socket.gaierror as exc:
        print(f"Lookup failed: {exc}")


def whois_query(domain, timeout=10):
    tld = domain.rsplit(".", 1)[-1].lower()
    server = WHOIS_SERVERS.get(tld, "whois.iana.org")
    print(f"\n--- WHOIS for {domain} (via {server}) ---")
    try:
        with socket.create_connection((server, 43), timeout=timeout) as s:
            s.sendall((domain + "\r\n").encode("utf-8"))
            chunks = []
            while True:
                data = s.recv(4096)
                if not data:
                    break
                chunks.append(data)
        text = b"".join(chunks).decode("utf-8", errors="replace")
    except Exception as exc:
        print(f"WHOIS failed: {exc}")
        return

    keep = ("registrar", "creation", "created", "expiry", "expires",
            "updated", "name server", "status", "registrant", "org")
    shown = False
    for line in text.splitlines():
        low = line.lower().strip()
        if any(low.startswith(k) for k in keep):
            print("  " + line.strip())
            shown = True
    if not shown:
        print(text.strip()[:1500])


def main():
    parser = argparse.ArgumentParser(description="DNS and WHOIS lookup tool.")
    parser.add_argument("domain", help="Domain to look up")
    parser.add_argument("--no-whois", action="store_true")
    args = parser.parse_args()

    domain = args.domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    if not domain:
        print("No domain given.")
        sys.exit(1)

    dns_records(domain)
    if not args.no_whois:
        whois_query(domain)


if __name__ == "__main__":
    main()
