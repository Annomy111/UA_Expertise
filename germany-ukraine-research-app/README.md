# Germany-Ukraine Contact Research App

Eine automatisierte Research-App zum Finden und Aktualisieren von Kontakten zur Ukraine-Arbeit in Deutschland.

## Features

- **Firebase/Firestore Backend**: Echtzeit-Datenbank mit Cloud-Sync
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

## Voraussetzungen

- Python 3.9+
- Self-hosted Firebase-Instanz mit Firestore
- Firebase Service Account Credentials

## Installation

### 1. Schnellinstallation (empfohlen)

```bash
cd germany-ukraine-research-app
./install.sh
```

Das Installations-Skript:
- Erstellt eine virtuelle Python-Umgebung
- Installiert alle Abhängigkeiten
- Erstellt die .env-Datei
- Initialisiert die Datenbank

### 2. Manuelle Installation

```bash
cd germany-ukraine-research-app

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Python-Abhängigkeiten installieren
pip install -r requirements.txt
```

### 3. Firebase-Konfiguration

**Wichtig:** Die App benötigt Zugriff auf Ihre self-hosted Firebase-Instanz.

1. **Service Account Credentials holen:**
   - Von Ihrer Firebase Console: Project Settings > Service Accounts
   - "Generate new private key" klicken
   - JSON-Datei herunterladen

2. **Credentials-Datei platzieren:**
   ```bash
   cp /pfad/zu/firebase-credentials.json config/firebase-config.json
   ```

3. **.env-Datei erstellen:**
   ```bash
   cp .env.example .env
   ```

4. **.env bearbeiten:**
   ```bash
   # Erforderlich: Pfad zu Firebase Credentials
   FIREBASE_CONFIG_PATH=config/firebase-config.json

   # Erforderlich: URL Ihrer Firebase-Instanz
   FIREBASE_URL=https://your-firebase-instance.com

   # Optional: Project ID
   FIREBASE_PROJECT_ID=your-project-id
   ```

**Ausführliche Firebase-Setup-Anleitung:** Siehe `config/FIREBASE_SETUP.md`

### 4. Datenbank initialisieren

```bash
python src/init_db.py
```

Sie sollten sehen:
```
✓ Firebase/Firestore initialisiert
  Verbunden mit: https://your-firebase-instance.com
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
