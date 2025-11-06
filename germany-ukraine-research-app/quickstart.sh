#!/bin/bash
# Schnellstart für Germany-Ukraine Contact Research

echo "🇺🇦 Germany-Ukraine Contact Research - Quickstart"
echo "===================================================="

# Installation falls nötig
if [ ! -d "venv" ]; then
    echo ""
    echo "Führe Installation durch..."
    ./install.sh
fi

# Aktiviere virtuelle Umgebung
source venv/bin/activate

# Prüfe ob Datenbank Daten hat
if [ ! -f "data/contacts.db" ] || [ $(sqlite3 data/contacts.db "SELECT COUNT(*) FROM contacts;" 2>/dev/null || echo "0") -eq 0 ]; then
    echo ""
    echo "Keine Daten gefunden - führe ersten Scan durch..."
    python src/scraper.py
else
    echo ""
    echo "✓ Datenbank mit Daten vorhanden"
fi

# Starte Web-App
echo ""
echo "===================================================="
echo "🌐 Starte Web-Interface..."
echo "Verfügbar unter: http://localhost:5000"
echo "Drücke Ctrl+C zum Beenden"
echo "===================================================="
echo ""

python src/app.py
