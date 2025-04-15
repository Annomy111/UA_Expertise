#!/bin/bash

# Farben für Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Ukraine Experts Database - Git Push${NC}"
echo "====================================================="
echo

# Prüfen, ob git installiert ist
if ! command -v git >/dev/null 2>&1; then
    echo -e "${RED}Git ist nicht installiert!${NC}"
    echo -e "${YELLOW}Bitte installiere Git: https://git-scm.com/downloads${NC}"
    exit 1
fi

# Prüfen, ob wir uns in einem Git-Repository befinden
if [ ! -d .git ]; then
    echo -e "${YELLOW}Kein Git-Repository gefunden. Initialisiere neues Repository...${NC}"
    git init
    echo -e "${GREEN}✓ Neues Git-Repository initialisiert${NC}"
else
    echo -e "${GREEN}✓ Git-Repository gefunden${NC}"
fi

# Docker-Komponenten identifizieren und zur .gitignore hinzufügen
echo -e "${YELLOW}Stelle sicher, dass Docker-Komponenten in .gitignore enthalten sind...${NC}"
grep -q "Dockerfile" .gitignore || echo "Dockerfile" >> .gitignore
grep -q "docker-compose.yml" .gitignore || echo "docker-compose.yml" >> .gitignore
echo -e "${GREEN}✓ .gitignore aktualisiert${NC}"

# Git Remote abfragen wenn nicht vorhanden
if ! git remote -v | grep -q origin; then
    echo -e "${YELLOW}Kein Git Remote 'origin' gefunden.${NC}"
    read -p "Git-Repository-URL eingeben (z.B. https://github.com/username/repo.git): " REPO_URL
    
    if [ -z "$REPO_URL" ]; then
        echo -e "${RED}Keine URL angegeben. Fahre ohne Remote fort.${NC}"
    else
        git remote add origin $REPO_URL
        echo -e "${GREEN}✓ Remote 'origin' hinzugefügt: $REPO_URL${NC}"
    fi
else
    echo -e "${GREEN}✓ Git Remote 'origin' gefunden${NC}"
fi

# Dateien zum Staging-Bereich hinzufügen
echo -e "${YELLOW}Füge Dateien zum Staging-Bereich hinzu...${NC}"
git add .
echo -e "${GREEN}✓ Dateien hinzugefügt${NC}"

# Abfrage für Commit-Nachricht
read -p "Commit-Nachricht eingeben (Standard: 'Remove Docker components and push to Git'): " COMMIT_MSG
COMMIT_MSG=${COMMIT_MSG:-"Remove Docker components and push to Git"}

# Commit erstellen
echo -e "${YELLOW}Erstelle Commit...${NC}"
git commit -m "$COMMIT_MSG"
echo -e "${GREEN}✓ Commit erstellt${NC}"

# Push zu Remote, wenn möglich
if git remote -v | grep -q origin; then
    echo -e "${YELLOW}Pushe zu Remote-Repository...${NC}"
    read -p "Branch-Namen eingeben (Standard: main): " BRANCH_NAME
    BRANCH_NAME=${BRANCH_NAME:-main}
    
    if git push -u origin $BRANCH_NAME; then
        echo -e "${GREEN}✓ Push erfolgreich!${NC}"
    else
        echo -e "${RED}✗ Push fehlgeschlagen!${NC}"
        echo -e "${YELLOW}Du kannst später manuell pushen mit: git push -u origin $BRANCH_NAME${NC}"
    fi
else
    echo -e "${YELLOW}Kein Remote 'origin' konfiguriert. Überspringe Push.${NC}"
    echo -e "${YELLOW}Wenn du später pushen möchtest, füge ein Remote hinzu mit: git remote add origin <url>${NC}"
    echo -e "${YELLOW}und führe dann aus: git push -u origin main${NC}"
fi

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}Git-Prozess abgeschlossen!${NC}"
echo -e "${GREEN}====================================================${NC}" 