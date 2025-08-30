import csv
import requests

CALLSIGN = "PD8GB"
LIMIT = 50
CSV_URL = f"https://wsprnet.org/olddb?band=all&call={CALLSIGN}&limit={LIMIT}&format=csv"
OUTPUT_FILE = "wspr_pd8gb.html"

response = requests.get(CSV_URL)
lines = response.text.splitlines()
reader = csv.DictReader(lines)

html = """<html><head>
<style>
body { background-color: #000; color: #fff; font-family: sans-serif; }
table { width: 100%; border-collapse: collapse; margin-top: 20px; }
th, td { padding: 6px; border-bottom: 1px solid #444; text-align: center; }
th { background-color: #222; color: #e74c3c; }
</style>
</head><body>
<h3 style="text-align:center; color:#e74c3c;">Laatste 50 WSPR spots van PD8GB</h3>
<table>
<tr><th>Tijd (UTC)</th><th>Frequentie</th><th>SNR</th><th>Afstand</th><th>Reporter</th></tr>
"""

for row in reader:
    html += f"<tr><td>{row['UTC']}</td><td>{row['Freq']}</td><td>{row['SNR']} dB</td><td>{row['km']} km</td><td>{row['Reporter']}</td></tr>\n"

html += "</table><p style='text-align:center; margin-top:20px;'>Data automatisch geladen van WSPRnet.org</p></body></html>"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ HTML gegenereerd: {OUTPUT_FILE}")
