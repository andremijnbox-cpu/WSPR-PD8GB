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
    line = line.strip()
    if line.startswith("20") and "PD8GB" in line:
        parts = line.split()
        if len(parts) >= 15:
            tijd      = parts[0] + " " + parts[1]          # Datum + Tijd
            freq      = parts[3]                           # Frequentie
            snr       = parts[4] + " dB"                   # SNR
            reporter  = parts[9]                           # Reporter callsign
            locator   = parts[10]                          # Reporter grid
            afstand   = parts[11] + " km"                  # Afstand
            rows.append((tijd, freq, snr, reporter, locator, afstand))

# 📝 Genereer HTML-bestand in docs/
with open("docs/wspr_pd8gb.html", "w") as f:
    f.write("""<html><head>
    <meta charset="UTF-8">
    <title>WSPR Spots van PD8GB</title>
    <style>
    body { background-color: #000; color: #fff; font-family: Arial, sans-serif; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 8px; border-bottom: 1px solid #444; text-align: center; }
    th { background-color: #222; color: #e74c3c; }
    h3 { text-align: center; color: #e74c3c; }
    </style></head><body>
    <h3>Laatste 50 WSPR spots van PD8GB</h3>
    <table>
    <tr><th>Tijd (UTC)</th><th>Frequentie</th><th>SNR</th><th>Reporter</th><th>Locatie</th><th>Afstand</th></tr>
    """)

    for row in rows:
        f.write(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>\n")

    f.write("</table></body></html>")
