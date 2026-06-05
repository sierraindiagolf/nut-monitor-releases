#!/bin/bash
set -e

# Create opt directory
mkdir -p /opt/nut-dashboard
mv /tmp/dashboard.py /opt/nut-dashboard/dashboard.py
chown -R nut:nut /opt/nut-dashboard
chmod 750 /opt/nut-dashboard
chmod 740 /opt/nut-dashboard/dashboard.py

# Create systemd service file
cat << 'EOF' > /etc/systemd/system/nut-dashboard.service
[Unit]
Description=NUT UPS Web Dashboard
After=nut-server.service mnt-usb_logs.mount
Requires=mnt-usb_logs.mount

[Service]
Type=simple
User=nut
Group=nut
WorkingDirectory=/opt/nut-dashboard
ExecStart=/usr/bin/python3 /opt/nut-dashboard/dashboard.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload and enable service
systemctl daemon-reload
systemctl enable nut-dashboard.service
systemctl restart nut-dashboard.service

echo "NUT Dashboard has been deployed and started successfully on port 8080."
