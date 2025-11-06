#!/bin/bash
# Führe Scraper aus

echo "🔍 Starte Web-Scraper..."
echo ""

# Aktiviere virtuelle Umgebung
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Führe Scraper aus
python src/scraper.py

echo ""
echo "✓ Scraping abgeschlossen"
