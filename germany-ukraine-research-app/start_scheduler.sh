#!/bin/bash
# Starte Scheduler für automatische Updates

echo "🤖 Starte automatischen Update-Scheduler..."
echo ""

# Aktiviere virtuelle Umgebung
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Starte Scheduler
echo "Scheduler läuft - Updates werden automatisch durchgeführt"
echo "Drücke Ctrl+C zum Beenden"
echo ""

python src/scheduler.py
