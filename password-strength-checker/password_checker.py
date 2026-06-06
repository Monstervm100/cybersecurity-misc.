import hashlib
import math
import re
import urllib.request
from getpass import getpass

COMMON = {
    "123456", "password", "123456789", "12345678", "12345", "qwerty",
    "abc123", "111111", "123123", "admin", "letmein", "welcome",
    "monkey", "dragon", "iloveyou", "sunshine", "princess", "football",
    "password1", "000000", "qwerty123", "1q2w3e4r", "superman",
}


def char_space(pw):
    space = 0
    if re.search(r"[a-z]", pw):
        space += 26
    if re.search(r"[A-Z]", pw):
        space += 26
    if re.search(r"[0-9]", pw):
        space += 10
    if re.search(r"[^A-Za-z0-9]", pw):
        space += 33
    return space


def entropy_bits(pw):
    space = char_space(pw)
    if space == 0:
        return 0.0
    return round(len(pw) * math.log2(space), 1)


def pattern_flags(pw):
    flags = []
    low = pw.lower()
    if low in COMMON:
        flags.append("appears in the common-password list")
    if re.search(r"(.)\1\1", pw):
        flags.append("contains a character repeated 3+ times")
    if re.search(r"(012|123|234|345|456|567|678|789|890)", pw):
        flags.append("contains a numeric sequence")
    if re.search(r"(qwer|asdf|zxcv|wert|sdfg)", low):
        flags.append("contains a keyboard walk")
    if re.search(r"(19|20)\d\d", pw):
        flags.append("contains something that looks like a year")
    return flags


def breach_count(pw):
    digest = hashlib.sha1(pw.encode("utf-8")).hexdigest().upper()
    prefix, suffix = digest[:5], digest[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "pw-checker/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
    except Exception:
        return None
    for line in body.splitlines():
        h, _, count = line.partition(":")
        if h.strip() == suffix:
            return int(count.strip())
    return 0


def rating(bits, flags, breached):
    if breached:
        return "CRITICAL"
    if flags or bits < 40:
        return "WEAK"
    if bits < 60:
        return "FAIR"
    if bits < 80:
        return "STRONG"
    return "EXCELLENT"


def suggestions(pw, bits, flags):
    out = []
    if len(pw) < 12:
        out.append("Use at least 12-16 characters.")
    if char_space(pw) < 62:
        out.append("Mix uppercase, lowercase, digits and symbols.")
    if flags:
        out.append("Avoid predictable patterns, sequences and common words.")
    if bits < 60:
        out.append("Prefer a long random passphrase of unrelated words.")
    if not out:
        out.append("Looks solid. Use a password manager and never reuse it.")
    return out


def main():
    pw = getpass("Enter a password to evaluate (input hidden): ")
    if not pw:
        print("No password entered.")
        return
    bits = entropy_bits(pw)
    flags = pattern_flags(pw)
    breached = breach_count(pw)

    print("\n--- Password Strength Report ---")
    print(f"Length        : {len(pw)}")
    print(f"Entropy       : {bits} bits")
    print(f"Character set : {char_space(pw)} possible symbols")
    if breached is None:
        print("Breach check  : unavailable (no network)")
    elif breached == 0:
        print("Breach check  : not found in known breaches")
    else:
        print(f"Breach check  : SEEN {breached:,} times in known breaches")
    print(f"Rating        : {rating(bits, flags, breached)}")
    if flags:
        print("Weaknesses    :")
        for f in flags:
            print(f"  - {f}")
    print("Suggestions   :")
    for s in suggestions(pw, bits, flags):
        print(f"  - {s}")


if __name__ == "__main__":
    main()
