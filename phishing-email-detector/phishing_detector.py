import argparse
import re
import sys
from email import policy
from email.parser import BytesParser

URGENT = ("urgent", "verify your account", "suspended", "act now", "immediately",
          "confirm your password", "unusual activity", "click here", "final notice",
          "your account will be", "update your payment")
SHORTENERS = ("bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd", "buff.ly")
URL_RE = re.compile(r'https?://[^\s"\'<>]+', re.I)
IP_URL_RE = re.compile(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', re.I)


def domain_of(addr):
    m = re.search(r"@([\w.-]+)", addr or "")
    return m.group(1).lower() if m else ""


def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    return part.get_content()
                except Exception:
                    return ""
    try:
        return msg.get_content()
    except Exception:
        return ""


def analyze(path):
    try:
        with open(path, "rb") as fh:
            msg = BytesParser(policy=policy.default).parse(fh)
    except Exception as exc:
        print(f"Cannot parse {path}: {exc}")
        sys.exit(1)

    findings = []
    from_hdr = str(msg.get("From", ""))
    reply_to = str(msg.get("Return-Path", "") or msg.get("Reply-To", ""))
    subject = str(msg.get("Subject", ""))

    from_dom = domain_of(from_hdr)
    reply_dom = domain_of(reply_to)
    if from_dom and reply_dom and from_dom != reply_dom:
        findings.append(f"From domain ({from_dom}) differs from reply/return ({reply_dom})")

    auth = str(msg.get("Authentication-Results", "")).lower()
    for mech in ("spf", "dkim", "dmarc"):
        if f"{mech}=fail" in auth or f"{mech}=softfail" in auth:
            findings.append(f"{mech.upper()} check failed in Authentication-Results")

    body = str(get_body(msg))
    blob = (subject + " " + body).lower()

    hits = [w for w in URGENT if w in blob]
    if hits:
        findings.append("Urgency/pressure language: " + ", ".join(hits[:5]))

    urls = URL_RE.findall(body)
    for u in urls:
        if any(s in u for s in SHORTENERS):
            findings.append(f"Link uses a URL shortener: {u}")
        if IP_URL_RE.match(u):
            findings.append(f"Link points to a raw IP address: {u}")

    for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*>([^<]+)</a>', body, re.I):
        href, text = m.group(1), m.group(2)
        if "http" in text.lower():
            hd = re.search(r"https?://([\w.-]+)", href)
            vd = re.search(r"https?://([\w.-]+)", text)
            if hd and vd and hd.group(1) != vd.group(1):
                findings.append(f"Display link {vd.group(1)} actually points to {hd.group(1)}")

    print("\n--- Phishing Analysis ---")
    print(f"From    : {from_hdr}")
    print(f"Subject : {subject}")
    print(f"URLs    : {len(urls)}")
    print(f"\nIndicators found: {len(findings)}")
    for f in findings:
        print(f"  ! {f}")
    score = min(100, len(findings) * 20)
    verdict = "LIKELY PHISHING" if score >= 60 else "SUSPICIOUS" if score >= 20 else "LOW RISK"
    print(f"\nRisk score : {score}/100  ->  {verdict}")


def main():
    parser = argparse.ArgumentParser(description="Phishing email indicator analyzer.")
    parser.add_argument("eml", help="Path to a .eml email file")
    args = parser.parse_args()
    analyze(args.eml)


if __name__ == "__main__":
    main()
