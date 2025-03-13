#!/bin/bash

# Set variables
BACKUP_DIR="../backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="ukraine_experts_backup_${TIMESTAMP}.sql"
CONTAINER_NAME="ukraine_experts_db"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup the database
echo "Backing up the database to ${BACKUP_DIR}/${BACKUP_FILE}..."
docker exec $CONTAINER_NAME pg_dump -U admin ukraine_experts > "${BACKUP_DIR}/${BACKUP_FILE}"

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully!"
    echo "Backup file: ${BACKUP_DIR}/${BACKUP_FILE}"
    
    # Compress the backup
    gzip "${BACKUP_DIR}/${BACKUP_FILE}"
    echo "Backup compressed: ${BACKUP_DIR}/${BACKUP_FILE}.gz"
else
    echo "Backup failed!"
fi 