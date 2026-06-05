#!/bin/bash
# Restore script for NUT Dashboard system
# Usage: sudo ./restore_system.sh /path/to/backup.tar.gz

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Error: Please run this script as root (sudo)."
  exit 1
fi

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: $0 /path/to/backup_file.tar.gz"
  exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: Backup file '$BACKUP_FILE' not found."
  exit 1
fi

echo "=== STEP 1: Installing Core Packages ==="
# Fallback dependencies if packages.txt isn't parsed, but we make sure they are installed:
REQUIRED_PACKAGES="nginx nut nut-client nut-server python3-bleak bluez bluez-tools bluetooth jq curl git usbutils python3"

echo "Running apt update..."
apt-get update

echo "Installing core packages: $REQUIRED_PACKAGES..."
apt-get install -y $REQUIRED_PACKAGES

echo "=== STEP 2: Extracting System Backup ==="
echo "Extracting $BACKUP_FILE to / ..."
tar -xzf "$BACKUP_FILE" -C /

# Set correct permissions just in case
chown -R nut:nut /opt/nut-dashboard
chmod 750 /opt/nut-dashboard
chmod 740 /opt/nut-dashboard/dashboard.py
chmod 740 /opt/nut-dashboard/ble_gateway.py
chmod 740 /opt/nut-dashboard/generate_ups_conf.py

echo "=== STEP 3: Initializing Configuration & Services ==="
echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Enabling custom services..."
systemctl enable nut-ups-dynamic-conf.service
systemctl enable nut-ble-gateway.service
systemctl enable nut-dashboard.service

echo "Running physical USB port resolver..."
systemctl start nut-ups-dynamic-conf.service || true

echo "Restarting services..."
systemctl restart nut-driver.target || true
systemctl restart nut-server || true
systemctl restart nginx || true
systemctl restart nut-monitor || true
systemctl restart nut-ble-gateway || true
systemctl restart nut-dashboard || true

echo "=== RESTORE COMPLETED SUCCESSFULLY ==="
echo "Please verify by visiting the web interface."
