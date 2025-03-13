#!/bin/bash

# Check if backup file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <backup_file>"
    echo "Example: $0 ../backups/ukraine_experts_backup_20230101_120000.sql.gz"
    exit 1
fi

BACKUP_FILE=$1
CONTAINER_NAME="ukraine_experts_db"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file '$BACKUP_FILE' not found!"
    exit 1
fi

# Check if the file is compressed
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "Decompressing backup file..."
    gunzip -c "$BACKUP_FILE" > "${BACKUP_FILE%.gz}"
    BACKUP_FILE="${BACKUP_FILE%.gz}"
    echo "Decompressed to $BACKUP_FILE"
fi

# Confirm restoration
echo "WARNING: This will overwrite the current database!"
read -p "Are you sure you want to proceed? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restoration cancelled."
    exit 1
fi

# Restore the database
echo "Restoring database from $BACKUP_FILE..."
cat "$BACKUP_FILE" | docker exec -i $CONTAINER_NAME psql -U admin -d ukraine_experts

# Check if restoration was successful
if [ $? -eq 0 ]; then
    echo "Database restoration completed successfully!"
else
    echo "Database restoration failed!"
fi 