#!/bin/bash

# Farben für die Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Ukraine Experts Database - Deployment-Skript${NC}"
echo -e "${YELLOW}========================================${NC}"

# Überprüfen, ob Docker installiert ist
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker ist nicht installiert. Bitte installiere Docker und versuche es erneut.${NC}"
    exit 1
fi

# Überprüfen, ob Docker Compose installiert ist
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose ist nicht installiert. Bitte installiere Docker Compose und versuche es erneut.${NC}"
    exit 1
fi

echo -e "${GREEN}Starte das Deployment...${NC}"

# Bauen und Starten der Container
echo -e "${YELLOW}Baue und starte die Container...${NC}"
docker-compose up -d --build

# Überprüfen, ob alle Container laufen
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Alle Container wurden erfolgreich gestartet!${NC}"
    echo -e "${YELLOW}Die Anwendung ist unter folgenden URLs verfügbar:${NC}"
    echo -e "${GREEN}Frontend: http://localhost:3000${NC}"
    echo -e "${GREEN}API: http://localhost:8000${NC}"
    echo -e "${GREEN}API-Dokumentation: http://localhost:8000/docs${NC}"
    echo -e "${GREEN}PgAdmin: http://localhost:5050${NC}"
    echo -e "${YELLOW}PgAdmin-Zugangsdaten:${NC}"
    echo -e "${GREEN}E-Mail: admin@example.com${NC}"
    echo -e "${GREEN}Passwort: password${NC}"
else
    echo -e "${RED}Es gab ein Problem beim Starten der Container. Bitte überprüfe die Docker-Logs.${NC}"
    exit 1
fi

echo -e "${YELLOW}========================================${NC}"
echo -e "${GREEN}Deployment abgeschlossen!${NC}" 