#!/bin/bash

# Farben für Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Ukraine Experts Database - Lokales Setup${NC}"
echo "====================================================="
echo

# Prüfen, ob PostgreSQL installiert ist
if command -v psql >/dev/null 2>&1; then
    echo -e "${GREEN}✓ PostgreSQL ist installiert${NC}"
else
    echo -e "${RED}✗ PostgreSQL ist nicht installiert${NC}"
    echo -e "${YELLOW}Bitte installieren Sie PostgreSQL: https://www.postgresql.org/download/${NC}"
    exit 1
fi

# Prüfen, ob Python installiert ist
if command -v python3 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Python ist installiert${NC}"
else
    echo -e "${RED}✗ Python ist nicht installiert${NC}"
    echo -e "${YELLOW}Bitte installieren Sie Python 3.9+: https://www.python.org/downloads/${NC}"
    exit 1
fi

# Prüfen, ob Node.js installiert ist
if command -v node >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Node.js ist installiert${NC}"
else
    echo -e "${RED}✗ Node.js ist nicht installiert${NC}"
    echo -e "${YELLOW}Bitte installieren Sie Node.js 20+: https://nodejs.org/en/download/${NC}"
    exit 1
fi

echo -e "\n${YELLOW}Datenbank einrichten...${NC}"
read -p "PostgreSQL Benutzername (Standard: admin): " db_user
db_user=${db_user:-admin}
read -s -p "PostgreSQL Passwort (Standard: password): " db_pass
db_pass=${db_pass:-password}
echo
read -p "PostgreSQL Datenbankname (Standard: ukraine_experts): " db_name
db_name=${db_name:-ukraine_experts}
read -p "PostgreSQL Port (Standard: 5432): " db_port
db_port=${db_port:-5432}

# Datenbank erstellen
echo -e "${YELLOW}Datenbank wird erstellt...${NC}"
if psql -U postgres -c "SELECT 1 FROM pg_database WHERE datname = '$db_name'" | grep -q 1; then
    echo -e "${YELLOW}Datenbank $db_name existiert bereits${NC}"
else
    if psql -U postgres -c "CREATE DATABASE $db_name;" 2>/dev/null; then
        echo -e "${GREEN}✓ Datenbank $db_name erstellt${NC}"
    else
        echo -e "${RED}✗ Fehler beim Erstellen der Datenbank. Bitte manuell anlegen.${NC}"
    fi
fi

# Schema importieren
echo -e "${YELLOW}Datenbankschema wird importiert...${NC}"
if psql -U postgres -d $db_name -f db-schema.sql 2>/dev/null; then
    echo -e "${GREEN}✓ Datenbankschema importiert${NC}"
else
    echo -e "${RED}✗ Fehler beim Importieren des Schemas. Bitte manuell importieren.${NC}"
fi

# .env-Datei erstellen/aktualisieren
echo -e "\n${YELLOW}Umgebungsvariablen werden aktualisiert...${NC}"
cat > .env << EOL
# Datenbank-Konfiguration
POSTGRES_USER=$db_user
POSTGRES_PASSWORD=$db_pass
POSTGRES_DB=$db_name
DB_HOST=localhost
DB_PORT=$db_port

# API-Konfiguration
API_PORT=8000

# Frontend-Konfiguration
NEXT_PUBLIC_API_URL=http://localhost:8000
EOL
echo -e "${GREEN}✓ .env-Datei aktualisiert${NC}"

# Python-Abhängigkeiten installieren
echo -e "\n${YELLOW}Backend-Abhängigkeiten werden installiert...${NC}"
cd ukraine-experts-db
python3 -m pip install -r requirements.txt
echo -e "${GREEN}✓ Backend-Abhängigkeiten installiert${NC}"

# Node.js-Abhängigkeiten installieren
echo -e "\n${YELLOW}Frontend-Abhängigkeiten werden installiert...${NC}"
cd ../ukraine-experts-ui
npm install
echo -e "${GREEN}✓ Frontend-Abhängigkeiten installiert${NC}"

cd ..

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}Setup abgeschlossen!${NC}"
echo
echo -e "${YELLOW}Um das Backend zu starten:${NC}"
echo "cd ukraine-experts-db && python3 -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000"
echo
echo -e "${YELLOW}Um das Frontend zu starten:${NC}"
echo "cd ukraine-experts-ui && npm run dev"
echo
echo -e "${GREEN}====================================================${NC}" 