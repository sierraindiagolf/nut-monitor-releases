#!/bin/bash
set -e

# Create log directory and set ownership to nut
mkdir -p /mnt/usb_logs/nut
chown -R nut:nut /mnt/usb_logs/nut
chmod 750 /mnt/usb_logs/nut

# Write upslog-ups1.service
cat << 'EOF' > /etc/systemd/system/upslog-ups1.service
[Unit]
Description=NUT UPS1 Logger
After=nut-server.service mnt-usb_logs.mount
Requires=mnt-usb_logs.mount

[Service]
Type=simple
User=nut
Group=nut
ExecStartPre=/bin/bash -c '[ -s /mnt/usb_logs/nut/ups1.csv ] || echo "timestamp,battery_charge_pct,battery_voltage,input_voltage,ups_load_pct,ups_status" > /mnt/usb_logs/nut/ups1.csv'
ExecStart=/usr/bin/upslog -F -s ups1@localhost -l /mnt/usb_logs/nut/ups1.csv -i 30 -f "%%TIME @Y-@m-@d @H:@M:@S%%,%%VAR battery.charge%%,%%VAR battery.voltage%%,%%VAR input.voltage%%,%%VAR ups.load%%,%%VAR ups.status%%"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Write upslog-ups2.service
cat << 'EOF' > /etc/systemd/system/upslog-ups2.service
[Unit]
Description=NUT UPS2 Logger
After=nut-server.service mnt-usb_logs.mount
Requires=mnt-usb_logs.mount

[Service]
Type=simple
User=nut
Group=nut
ExecStartPre=/bin/bash -c '[ -s /mnt/usb_logs/nut/ups2.csv ] || echo "timestamp,battery_charge_pct,battery_voltage,input_voltage,ups_load_pct,ups_status" > /mnt/usb_logs/nut/ups2.csv'
ExecStart=/usr/bin/upslog -F -s ups2@localhost -l /mnt/usb_logs/nut/ups2.csv -i 30 -f "%%TIME @Y-@m-@d @H:@M:@S%%,%%VAR battery.charge%%,%%VAR battery.voltage%%,%%VAR input.voltage%%,%%VAR ups.load%%,%%VAR ups.status%%"
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and restart the services
systemctl daemon-reload
systemctl restart upslog-ups1.service upslog-ups2.service

echo "Logging services have been updated with CSV headers."
