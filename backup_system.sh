#!/bin/bash
# Backup script for NUT Dashboard system
# Saves package list, configurations, systemd services, and source code.
set -e

BACKUP_DIR="/mnt/usb_logs/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/nut_system_backup_${TIMESTAMP}.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Updating list of installed packages..."
apt-mark showmanual > /opt/nut-dashboard/packages.txt

echo "Starting backup to ${BACKUP_FILE}..."

# Create compressed tar archive of configuration files, scripts, and code
tar -czf "$BACKUP_FILE" \
    /etc/nut \
    /etc/nginx \
    /etc/systemd/system/nut-dashboard.service \
    /etc/systemd/system/nut-ble-gateway.service \
    /etc/systemd/system/nut-ups-dynamic-conf.service \
    /opt/nut-dashboard \
    /etc/fstab

echo "Backup completed successfully!"

# Keep only the last 7 backups to prevent space issues
find "$BACKUP_DIR" -name "nut_system_backup_*.tar.gz" -type f -mtime +7 -delete
echo "Cleaned up backups older than 7 days."
