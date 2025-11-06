#!/bin/bash
# Starte Flask-Web-App

echo "🌐 Starte Web-Interface..."
echo ""

# Aktiviere virtuelle Umgebung
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Starte Flask-App
echo "Web-Interface verfügbar unter: http://localhost:5000"
echo "Drücke Ctrl+C zum Beenden"
echo ""

python src/app.py
