#!/usr/bin/env python3
"""
Initialisiere Firebase/Firestore für Germany-Ukraine Contact Research
"""

import os
from dotenv import load_dotenv
from database import db_manager

# Lade Umgebungsvariablen
load_dotenv()


def main():
    """Hauptfunktion"""
    print("🔧 Initialisiere Firebase/Firestore Verbindung...")
    print("")

    # Prüfe ob Firebase-Konfiguration vorhanden
    firebase_config = os.getenv('FIREBASE_CONFIG_PATH', 'config/firebase-config.json')
    if not os.path.exists(firebase_config):
        print("⚠️  WARNUNG: Firebase-Konfiguration nicht gefunden!")
        print(f"   Erwartet: {firebase_config}")
        print("")
        print("Bitte:")
        print("1. Erstelle config/firebase-config.json mit deinen Firebase Credentials")
        print("2. Oder setze FIREBASE_CONFIG_PATH in .env")
        print("")
        print("Siehe config/FIREBASE_SETUP.md für Details")
        return

    try:
        db_manager.initialize()
        print("")
        print("✓ Firebase/Firestore erfolgreich initialisiert")
        print("")

        # Zeige Statistiken
        stats = db_manager.get_statistics()
        print(f"📊 Aktuelle Datenbank:")
        print(f"   Kontakte: {stats['total_contacts']}")
        if stats['by_type']:
            print("   Nach Typ:")
            for contact_type, count in stats['by_type'].items():
                print(f"      - {contact_type}: {count}")

        print("")
        print("Nächste Schritte:")
        print("1. Führe ersten Scan durch: python src/scraper.py")
        print("2. Starte Web-Interface: python src/app.py")
        print("3. Oder nutze Quickstart: ./quickstart.sh")

    except Exception as e:
        print("")
        print(f"✗ Fehler bei der Initialisierung: {e}")
        print("")
        print("Mögliche Lösungen:")
        print("1. Prüfe deine Firebase-Konfiguration in config/firebase-config.json")
        print("2. Stelle sicher, dass FIREBASE_URL in .env gesetzt ist")
        print("3. Siehe config/FIREBASE_SETUP.md für Details")


if __name__ == '__main__':
    main()
