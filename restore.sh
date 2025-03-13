#!/bin/bash

# Farben für die Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Ukraine Experts Database - Wiederherstellungs-Skript${NC}"
echo -e "${YELLOW}========================================${NC}"

# Überprüfen, ob ein Backup-Dateiname als Parameter übergeben wurde
if [ -z "$1" ]; then
    echo -e "${RED}Fehler: Kein Backup-Dateiname angegeben.${NC}"
    echo -e "${YELLOW}Verwendung: $0 <backup-datei>${NC}"
    echo -e "${YELLOW}Verfügbare Backups:${NC}"
    ls -lh ./backups/*.gz 2>/dev/null || echo -e "${RED}Keine Backups gefunden.${NC}"
    exit 1
fi

BACKUP_FILE="$1"

# Überprüfen, ob die Backup-Datei existiert
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Fehler: Backup-Datei '$BACKUP_FILE' nicht gefunden.${NC}"
    exit 1
fi

echo -e "${YELLOW}Wiederherstellung aus Backup: $BACKUP_FILE${NC}"

# Wenn die Datei komprimiert ist, entpacken
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo -e "${GREEN}Entpacke komprimiertes Backup...${NC}"
    gunzip -c "$BACKUP_FILE" > /tmp/restore_temp.sql
    RESTORE_FILE="/tmp/restore_temp.sql"
else
    RESTORE_FILE="$BACKUP_FILE"
fi

echo -e "${GREEN}Stelle Datenbank wieder her...${NC}"
echo -e "${YELLOW}WARNUNG: Alle vorhandenen Daten werden überschrieben!${NC}"
read -p "Möchtest du fortfahren? (j/n): " CONFIRM

if [[ "$CONFIRM" != "j" && "$CONFIRM" != "J" ]]; then
    echo -e "${YELLOW}Wiederherstellung abgebrochen.${NC}"
    exit 0
fi

# Führe den Wiederherstellungsbefehl aus
cat "$RESTORE_FILE" | docker exec -i ukraine_experts_db psql -U admin -d ukraine_experts

# Überprüfe, ob die Wiederherstellung erfolgreich war
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Datenbank erfolgreich wiederhergestellt!${NC}"
else
    echo -e "${RED}Fehler bei der Wiederherstellung der Datenbank.${NC}"
    exit 1
fi

# Temporäre Datei löschen, wenn sie erstellt wurde
if [[ "$BACKUP_FILE" == *.gz ]]; then
    rm -f "$RESTORE_FILE"
fi

echo -e "${YELLOW}========================================${NC}"
echo -e "${GREEN}Wiederherstellung abgeschlossen!${NC}" 