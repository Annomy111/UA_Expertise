# Firebase Setup für Germany-Ukraine Contact Research App

Diese Anleitung hilft Ihnen, Ihre self-hosted Firebase-Instanz mit der App zu verbinden.

## Voraussetzungen

- Eine laufende self-hosted Firebase-Instanz
- Service Account Credentials (JSON-Datei)
- Firestore Datenbank aktiviert

## Setup-Schritte

### 1. Service Account Credentials

Holen Sie sich Ihre Firebase Service Account Credentials von Ihrer Firebase-Instanz:

1. Gehen Sie zu Ihrer Firebase Console
2. Navigieren Sie zu **Project Settings** > **Service Accounts**
3. Klicken Sie auf **Generate new private key**
4. Speichern Sie die JSON-Datei

### 2. Konfigurationsdatei erstellen

Kopieren Sie die heruntergeladene Credentials-Datei:

```bash
cd germany-ukraine-research-app/config
cp /pfad/zu/ihrer/firebase-credentials.json firebase-config.json
```

Alternativ können Sie die Beispieldatei verwenden und anpassen:

```bash
cp firebase-config.example.json firebase-config.json
# Bearbeiten Sie firebase-config.json mit Ihren echten Credentials
```

### 3. Umgebungsvariablen setzen

Bearbeiten Sie die `.env` Datei (oder erstellen Sie sie):

```bash
# Firebase-Konfiguration
FIREBASE_CONFIG_PATH=config/firebase-config.json

# Für self-hosted Firebase: URL Ihrer Firebase-Instanz
FIREBASE_URL=https://your-firebase-instance.com

# Optional: Firebase Project ID
FIREBASE_PROJECT_ID=your-project-id
```

### 4. Firestore-Datenbank

Stellen Sie sicher, dass in Ihrer Firebase-Instanz Firestore aktiviert ist.

Die App erstellt automatisch folgende Collections:
- `contacts` - Kontaktdaten
- `search_logs` - Such-Logs

### 5. Sicherheitsregeln (optional)

Für eine self-hosted Firebase-Instanz können Sie folgende Firestore-Sicherheitsregeln verwenden:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Contacts Collection - Read/Write für authentifizierte Service Accounts
    match /contacts/{contactId} {
      allow read, write: if request.auth != null;
    }

    // Search Logs - Write für authentifizierte Service Accounts
    match /search_logs/{logId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## Verbindung testen

Testen Sie die Verbindung mit:

```bash
python src/init_db.py
```

Sie sollten sehen:
```
✓ Firebase/Firestore initialisiert
  Verbunden mit: https://your-firebase-instance.com
```

## Fehlerbehebung

### Fehler: "Firebase-Konfiguration nicht gefunden"

**Lösung:** Stellen Sie sicher, dass `config/firebase-config.json` existiert oder setzen Sie `FIREBASE_CONFIG_PATH` in `.env`

### Fehler: "Permission denied"

**Lösung:**
- Prüfen Sie Ihre Service Account Permissions
- Stellen Sie sicher, dass Firestore aktiviert ist
- Überprüfen Sie Ihre Firestore-Sicherheitsregeln

### Fehler: "Connection timeout"

**Lösung:**
- Prüfen Sie Ihre `FIREBASE_URL` in `.env`
- Stellen Sie sicher, dass Ihre Firebase-Instanz erreichbar ist
- Prüfen Sie Firewall/Netzwerk-Einstellungen

## Self-Hosted Firebase Hinweise

Wenn Sie eine self-hosted Firebase-Instanz verwenden (z.B. Firebase Emulator Suite):

1. **Emulator Suite URL:**
   ```bash
   FIREBASE_URL=http://localhost:8080
   ```

2. **Firestore Emulator:**
   Stellen Sie sicher, dass der Firestore Emulator läuft:
   ```bash
   firebase emulators:start --only firestore
   ```

3. **Umgebungsvariable für Emulator:**
   ```bash
   export FIRESTORE_EMULATOR_HOST=localhost:8080
   ```

## Daten-Migration von SQLite

Falls Sie bereits Daten in SQLite haben und zu Firebase migrieren möchten, können Sie ein Migrations-Skript verwenden:

```bash
python scripts/migrate_sqlite_to_firebase.py
```

## Backup

Für Backups Ihrer Firebase-Daten:

```bash
# Export alle Kontakte
python src/export.py --format json

# Oder nutzen Sie Firebase-native Backup-Tools
```

## Support

Bei Problemen mit der Firebase-Integration:
1. Prüfen Sie die Logs
2. Testen Sie die Verbindung mit `python src/init_db.py`
3. Überprüfen Sie Ihre Credentials und Permissions
