import urllib.request
import re

codes = [
    ('15-1254.00', 'Web Developers'),
    ('15-1252.00', 'Software Developers'),
    ('15-2051.01', 'Business Intelligence Analysts'),
    ('15-2051.00', 'Data Scientists'),
    ('15-1253.00', 'Software Quality Assurance Analysts and Testers'),
    ('15-1244.00', 'Network and Computer Systems Administrators'),
    ('11-2021.00', 'Marketing Managers'),
    ('15-1255.00', 'Web and Digital Interface Designers'),
    ('15-1255.01', 'Video Game Designers'),
    ('13-1111.00', 'Management Analysts'),
    ('15-1243.00', 'Database Architects'),
    ('15-1243.01', 'Data Warehousing Specialists'),
    ('15-1212.00', 'Information Security Analysts')
]

print("Checking O*NET Online official pages:")
for code, expected in codes:
    url = f"https://www.onetonline.org/link/summary/{code}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'<title>(.*?)</title>', html, re.I)
            title = m.group(1).strip() if m else "Unknown"
            print(f"[{code}] -> {title}")
    except Exception as e:
        print(f"[{code}] -> FAILED: {e}")
