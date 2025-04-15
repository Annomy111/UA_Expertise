#!/bin/bash

# Farben für Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funktion zum Überprüfen, ob ein Prozess auf einem Port läuft
check_port() {
    if command -v lsof >/dev/null 2>&1; then
        lsof -i :$1 >/dev/null 2>&1
        return $?
    elif command -v netstat >/dev/null 2>&1; then
        netstat -tuln | grep $1 >/dev/null 2>&1
        return $?
    else
        # Wenn weder lsof noch netstat verfügbar ist, nehmen wir an, dass der Port frei ist
        return 1
    fi
}

echo -e "${GREEN}Ukraine Experts Database - Anwendung starten${NC}"
echo "====================================================="
echo

# Überprüfen, ob .env existiert
if [ ! -f .env ]; then
    echo -e "${RED}Keine .env-Datei gefunden!${NC}"
    echo -e "${YELLOW}Bitte führen Sie zuerst das Setup-Skript aus: ./setup.sh${NC}"
    exit 1
fi

# Überprüfen, ob Ports bereits belegt sind
if check_port 8000; then
    echo -e "${RED}Port 8000 (API) ist bereits belegt!${NC}"
    echo -e "${YELLOW}Bitte beenden Sie den entsprechenden Prozess oder ändern Sie den Port in .env${NC}"
    exit 1
fi

if check_port 3000; then
    echo -e "${RED}Port 3000 (Frontend) ist bereits belegt!${NC}"
    echo -e "${YELLOW}Bitte beenden Sie den entsprechenden Prozess oder ändern Sie den Port in .env${NC}"
    exit 1
fi

# Backend starten
echo -e "${YELLOW}Backend wird gestartet...${NC}"
cd ukraine-experts-db
python3 -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Warten bis der Backend-Server läuft
echo -e "${YELLOW}Warte bis das Backend bereit ist...${NC}"
i=0
while ! curl -s http://localhost:8000 >/dev/null; do
    sleep 1
    ((i=i+1))
    if [ $i -gt 10 ]; then
        echo -e "${RED}Timeout beim Warten auf das Backend!${NC}"
        kill $BACKEND_PID
        exit 1
    fi
done

echo -e "${GREEN}✓ Backend läuft auf http://localhost:8000${NC}"

# Frontend starten
echo -e "${YELLOW}Frontend wird gestartet...${NC}"
cd ukraine-experts-ui
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✓ Frontend wird auf http://localhost:3000 gestartet${NC}"

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}Anwendung läuft!${NC}"
echo -e "API: ${YELLOW}http://localhost:8000${NC}"
echo -e "UI: ${YELLOW}http://localhost:3000${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "Drücken Sie CTRL+C, um die Anwendung zu beenden..."

# Funktion zum Beenden aller Prozesse beim Schließen des Skripts
cleanup() {
    echo -e "\n${YELLOW}Beende alle Prozesse...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Anwendung wurde beendet.${NC}"
    exit 0
}

# Signal-Handler für sauberes Beenden
trap cleanup SIGINT SIGTERM

# Warten, bis der Benutzer das Skript beendet
wait 