#!/usr/bin/env python3
"""
Initialisiere Datenbank für Germany-Ukraine Contact Research
"""

from database import db_manager


def main():
    """Hauptfunktion"""
    print("🔧 Initialisiere Datenbank...")
    db_manager.initialize()
    print("✓ Datenbank erfolgreich initialisiert")
    print(f"   Speicherort: {db_manager.db_path}")
    print("\nNächste Schritte:")
    print("1. Führe ersten Scan durch: python src/scraper.py")
    print("2. Starte Web-Interface: python src/app.py")


if __name__ == '__main__':
    main()
