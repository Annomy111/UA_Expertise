#!/bin/bash
# Installations-Skript für Germany-Ukraine Contact Research

echo "🇺🇦 Germany-Ukraine Contact Research - Installation"
echo "===================================================="

# Prüfe Python-Version
echo ""
echo "Prüfe Python-Version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version gefunden"

# Erstelle virtuelle Umgebung
echo ""
echo "Erstelle virtuelle Umgebung..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtuelle Umgebung erstellt"
else
    echo "ℹ Virtuelle Umgebung existiert bereits"
fi

# Aktiviere virtuelle Umgebung
echo ""
echo "Aktiviere virtuelle Umgebung..."
source venv/bin/activate
echo "✓ Virtuelle Umgebung aktiviert"

# Installiere Abhängigkeiten
echo ""
echo "Installiere Python-Abhängigkeiten..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Abhängigkeiten installiert"

# Erstelle .env wenn nicht vorhanden
echo ""
if [ ! -f ".env" ]; then
    echo "Erstelle .env Datei..."
    cp .env.example .env
    echo "✓ .env Datei erstellt (bitte anpassen wenn nötig)"
else
    echo "ℹ .env Datei existiert bereits"
fi

# Initialisiere Datenbank
echo ""
echo "Initialisiere Datenbank..."
python src/init_db.py
echo "✓ Datenbank initialisiert"

# Fertig
echo ""
echo "===================================================="
echo "✓ Installation abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "1. (Optional) Passe .env an (z.B. SerpAPI-Key)"
echo "2. Führe ersten Scan durch: ./run_scraper.sh"
echo "3. Starte Web-Interface: ./start_app.sh"
echo ""
echo "Oder führe alles zusammen aus: ./quickstart.sh"
echo "===================================================="
