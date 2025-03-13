#!/bin/bash

# Farben für die Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Ukraine Experts Database - Backup-Skript${NC}"
echo -e "${YELLOW}========================================${NC}"

# Datum für den Backup-Dateinamen
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="./backups"
BACKUP_FILE="${BACKUP_DIR}/ukraine_experts_${DATE}.sql"

# Erstelle Backup-Verzeichnis, falls es nicht existiert
mkdir -p ${BACKUP_DIR}

echo -e "${GREEN}Erstelle Backup der Datenbank...${NC}"

# Führe den Backup-Befehl aus
docker exec ukraine_experts_db pg_dump -U admin ukraine_experts > ${BACKUP_FILE}

# Überprüfe, ob das Backup erfolgreich war
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Backup erfolgreich erstellt: ${BACKUP_FILE}${NC}"
    
    # Komprimiere das Backup
    echo -e "${YELLOW}Komprimiere Backup...${NC}"
    gzip ${BACKUP_FILE}
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Backup komprimiert: ${BACKUP_FILE}.gz${NC}"
        echo -e "${YELLOW}Backup-Größe: $(du -h ${BACKUP_FILE}.gz | cut -f1)${NC}"
    else
        echo -e "${RED}Fehler beim Komprimieren des Backups.${NC}"
    fi
else
    echo -e "${RED}Fehler beim Erstellen des Backups.${NC}"
    exit 1
fi

echo -e "${YELLOW}========================================${NC}"
echo -e "${GREEN}Backup abgeschlossen!${NC}" 