#!/bin/bash
set -e

# Write real UPS configurations to ups.conf
cat << 'EOF' > /etc/nut/ups.conf
maxretry = 3

[ups1]
    driver = nutdrv_qx
    port = auto
    vendorid = 0665
    productid = 5161
    bus = 005
    desc = "First UPS"

[ups2]
    driver = nutdrv_qx
    port = auto
    vendorid = 0665
    productid = 5161
    bus = 006
    desc = "Second UPS"
EOF

# Make sure permissions are correct
chown root:nut /etc/nut/ups.conf
chmod 640 /etc/nut/ups.conf

# Restart the driver enumerator and the server
echo "Restarting NUT drivers and server..."
systemctl restart nut-driver.target nut-server

# Wait 3 seconds for the drivers to initialize and connect
sleep 3

# Query devices and output
echo "=== UPS 1 status ==="
upsc ups1@localhost || true

echo "=== UPS 2 status ==="
upsc ups2@localhost || true
