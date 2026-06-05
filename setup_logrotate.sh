#!/bin/bash
set -e

# Create logrotate configuration for NUT logs
cat << 'EOF' > /etc/logrotate.d/nut-usb-logs
/mnt/usb_logs/nut/*.csv {
    daily
    rotate 30
    missingok
    notifempty
    compress
    delaycompress
    sharedscripts
    postrotate
        systemctl restart upslog-ups1.service upslog-ups2.service >/dev/null 2>&1 || true
    endscript
}
EOF

# Set permissions for logrotate config (must be owned by root, 644)
chown root:root /etc/logrotate.d/nut-usb-logs
chmod 644 /etc/logrotate.d/nut-usb-logs

# Force run logrotate to test the configuration
logrotate -f /etc/logrotate.d/nut-usb-logs

echo "Log rotation has been successfully configured and tested."
