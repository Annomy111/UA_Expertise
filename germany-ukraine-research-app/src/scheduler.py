#!/usr/bin/env python3
"""
Scheduler für automatische Updates
"""

import schedule
import time
from scraper import ContactScraper
from datetime import datetime


def run_update():
    """Führe Update durch"""
    print(f"\n{'='*60}")
    print(f"🕐 Automatisches Update gestartet: {datetime.now()}")
    print(f"{'='*60}\n")

    scraper = ContactScraper()
    scraper.update_contacts()

    print(f"\n{'='*60}")
    print(f"✓ Update abgeschlossen: {datetime.now()}")
    print(f"{'='*60}\n")


def main():
    """Hauptfunktion"""
    print("🤖 Scheduler gestartet")
    print("Automatische Updates werden täglich durchgeführt")
    print("Drücke Ctrl+C zum Beenden\n")

    # Führe erstes Update sofort aus
    run_update()

    # Schedule tägliche Updates um 2:00 Uhr
    schedule.every().day.at("02:00").do(run_update)

    # Optional: Wöchentliches vollständiges Update
    schedule.every().sunday.at("03:00").do(run_update)

    # Loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Prüfe jede Minute


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler beendet")
