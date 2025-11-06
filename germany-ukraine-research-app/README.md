# Germany-Ukraine Contact Research App

Eine automatisierte Research-App zum Finden und Aktualisieren von Kontakten zur Ukraine-Arbeit in Deutschland.

## Features

- **Automatische Web-Recherche**: Findet aktuelle Organisationen, NGOs, Think Tanks und Initiativen
- **Multi-Source Datensammlung**: Sammelt Daten aus verschiedenen Quellen
- **Automatische Updates**: Hält die Kontaktdaten immer aktuell
- **Suchfunktion**: Durchsuchbare Datenbank aller Kontakte
- **Export-Funktion**: Exportiere Daten als CSV, JSON oder Excel

## Quellen

Die App durchsucht automatisch:
- Deutsche Ministerien und Behörden mit Ukraine-Bezug
- NGOs und Hilfsorganisationen
- Think Tanks und Forschungseinrichtungen
- Universitäten mit Ukraine-Forschung
- Medienorganisationen mit Ukraine-Fokus
- Lokale Initiativen und Vereine

## Installation

```bash
cd germany-ukraine-research-app

# Python-Abhängigkeiten installieren
pip install -r requirements.txt

# Datenbank initialisieren
python src/init_db.py

# Erste Datensammlung durchführen
python src/scraper.py
```

## Verwendung

### Manuelle Suche durchführen
```bash
python src/scraper.py
```

### Automatische Updates einrichten (täglich)
```bash
python src/scheduler.py
```

### Web-Interface starten
```bash
python src/app.py
```

Die App ist dann verfügbar unter: http://localhost:5000

### Daten exportieren
```bash
python src/export.py --format csv
python src/export.py --format json
python src/export.py --format excel
```

## Konfiguration

Passe die Datei `config/sources.yaml` an, um:
- Neue Datenquellen hinzuzufügen
- Suchparameter zu ändern
- Update-Intervalle anzupassen

## Datenschutz

Diese App sammelt nur öffentlich verfügbare Informationen. Beachte die DSGVO-Richtlinien bei der Verwendung der gesammelten Daten.

## Lizenz

MIT
