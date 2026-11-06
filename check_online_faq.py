#!/usr/bin/env python3
"""Check if online faq.html has been deployed with fixes."""

import urllib.request
import sys

URL = "https://kdelec.com/faq.html"

try:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read().decode("utf-8", errors="replace")
except Exception as e:
    print(f"Failed to fetch {URL}: {e}")
    sys.exit(1)

# Check critical locations
idx1 = content.find("Yiwu, China")
if idx1 >= 0:
    snippet1 = content[idx1 : idx1 + 60]
    print(f"Address area: {repr(snippet1)}")

idx2 = content.find("Phone/WhatsApp/WeChat")
if idx2 >= 0:
    snippet2 = content[idx2 - 30 : idx2 + 40]
    print(f"Contact area: {repr(snippet2)}")

has_garbled_emdash = "攖" in content or "鈥" in content[: content.find("Yiwu, China") + 100] if "Yiwu, China" in content else False
has_garbled_emoji = "馃" in content or "鉁" in content

print(f"\nOnline has garbled em-dash: {has_garbled_emdash}")
print(f"Online has garbled emoji: {has_garbled_emoji}")

if not has_garbled_emdash and not has_garbled_emoji:
    print("\nONLINE IS FIXED — issue is browser/CDN cache")
else:
    print("\nONLINE STILL HAS GARBLED CHARS — Cloudflare Pages not deployed yet")
