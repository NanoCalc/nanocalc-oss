#!/bin/bash


SRC_FILE=~/src/nanocalc-oss/visitors.db
DEST_FILE=~/backup/visitors.db


if [ -f "$SRC_FILE" ]; then
    cp "$SRC_FILE" "$DEST_FILE"

    echo "Backup completed on $(date)" >> ~/backup/backup_log.txt
    echo "Backup completed successfully."
else
    echo "Backup failed on $(date)" >> ~/backup/backup_log.txt
    echo "Error: Source database file not found."
fi
