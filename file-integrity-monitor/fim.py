import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

BASELINE = "baseline.json"


def sha256_of(path, chunk=65536):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def walk(root):
    snapshot = {}
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            try:
                st = os.stat(full)
                snapshot[rel] = {
                    "sha256": sha256_of(full),
                    "size": st.st_size,
                    "mtime": round(st.st_mtime, 2),
                }
            except (OSError, PermissionError):
                continue
    return snapshot


def build(root):
    snap = walk(root)
    data = {
        "root": os.path.abspath(root),
        "created": datetime.now(timezone.utc).isoformat(),
        "files": snap,
    }
    with open(BASELINE, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
    print(f"Baseline written: {BASELINE} ({len(snap)} files)")


def check(root):
    if not os.path.exists(BASELINE):
        print(f"No baseline found. Run: python fim.py baseline {root}")
        sys.exit(1)
    with open(BASELINE, encoding="utf-8") as fh:
        old = json.load(fh)["files"]
    new = walk(root)

    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    modified = sorted(
        p for p in set(old) & set(new) if old[p]["sha256"] != new[p]["sha256"]
    )

    print(f"\n--- Integrity check against {BASELINE} ---")
    print(f"Added    : {len(added)}")
    for p in added:
        print(f"  + {p}")
    print(f"Removed  : {len(removed)}")
    for p in removed:
        print(f"  - {p}")
    print(f"Modified : {len(modified)}")
    for p in modified:
        print(f"  ~ {p}")
    if not (added or removed or modified):
        print("\nNo changes detected. Integrity intact.")
    else:
        print("\nChanges detected.")


def main():
    parser = argparse.ArgumentParser(description="Hash-based file integrity monitor.")
    parser.add_argument("mode", choices=["baseline", "check"])
    parser.add_argument("path", help="Directory to monitor")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Not a directory: {args.path}")
        sys.exit(1)
    if args.mode == "baseline":
        build(args.path)
    else:
        check(args.path)


if __name__ == "__main__":
    main()
