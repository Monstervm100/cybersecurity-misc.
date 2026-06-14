import argparse
import socket
import threading
from datetime import datetime, timezone

LOGFILE = "honeypot.log"
BANNER = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n"
log_lock = threading.Lock()


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()}  {msg}"
    print(line)
    with log_lock:
        with open(LOGFILE, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def handle(conn, addr):
    ip, port = addr
    try:
        conn.settimeout(10)
        conn.sendall(BANNER)
        data = conn.recv(512)
        client_id = data.decode("utf-8", errors="replace").strip()
        log(f"CONNECT  {ip}:{port}  client_id={client_id!r}")
    except Exception as exc:
        log(f"CONNECT  {ip}:{port}  (no handshake: {exc})")
    finally:
        try:
            conn.close()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Low-interaction SSH honeypot.")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=2222)
    args = parser.parse_args()

    print("=" * 60)
    print("  SSH HONEYPOT - deploy ONLY on infrastructure you own.")
    print("  It logs connection attempts. It grants NO shell or real")
    print("  access to any system.")
    print("=" * 60)

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind((args.host, args.port))
    except PermissionError:
        print(f"Cannot bind {args.host}:{args.port} (try a port >1024 or run elevated).")
        return
    srv.listen(50)
    log(f"START honeypot listening on {args.host}:{args.port}")

    try:
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        log("STOP honeypot")
    finally:
        srv.close()


if __name__ == "__main__":
    main()
