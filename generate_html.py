import requests
from bs4 import BeautifulSoup
import os

# 📁 Zorg dat de docs/ folder bestaat
os.makedirs("docs", exist_ok=True)

# 🚫 Zet Jekyll uit zodat GitHub Pages je HTML direct serveert
with open("docs/.nojekyll", "w") as f:
    f.write("")

# 🌐 Haal WSPR data op
url = "https://www.wsprnet.org/olddb?mode=html&band=all&limit=50&findcall=PD8GB&findreporter=&sort=date"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rows = []
for line in soup.get_text().splitlines():
    if "PD8GB" in line and line.strip():
        parts = line.split()
        if len(parts) >= 13:
            tijd = parts[0] + " " + parts[1]          # Datum + Tijd
            freq = parts[2]                           # Frequentie
            snr = parts[3]                            # SNR
            reporter = parts[8]                       # Reporter call
            locator = parts[9]                        # Locator van reporter
            afstand = parts[10]                       # Afstand in km
            rows.append((tijd, freq, snr, locator, afstand, reporter))

# 📝 Genereer HTML-bestand in docs/
with open("docs/wspr_pd8gb.html", "w") as f:
    f.write("""<html><head>
    <style>
    body { background-color: #000; color: #fff; font-family: sans-serif; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 6px; border-bottom: 1px solid #444; text-align: center; }
    th { background-color: #222; color: #e74c3c; }
    </style></head><body>
    <h3 style='text-align:center; color:#e74c3c;'>Laatste 50 WSPR spots van PD8GB</h3>
    <table>
    <tr><th>Tijd (UTC)</th><th>Frequentie</th><th>SNR</th><th>Locatie</th><th>Afstand</th><th>Reporter</th></tr>
    """)
    for row in rows:
        f.write(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]} dB</td><td>{row[3]}</td><td>{row[4]} km</td><td>{row[5]}</td></tr>\n")
    f.write("</table></body></html>")
