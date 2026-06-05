#!/bin/bash
set -e

# 1. Change Hostname
echo "Setting hostname to shoim-1.bavariaduo.home..."
hostnamectl set-hostname shoim-1.bavariaduo.home

# Update /etc/hosts
sed -i 's/127.0.1.1.*/127.0.1.1\tshoim-1.bavariaduo.home shoim-1/g' /etc/hosts
sed -i 's/::1\tlocalhost orangepizero3/::1\tlocalhost shoim-1.bavariaduo.home shoim-1/g' /etc/hosts

# 2. Update dashboard.py to bind to localhost only (security hardening)
echo "Hardening dashboard.py network binding to localhost only..."
sed -i "s/server = HTTPServer(('0.0.0.0', PORT), DashboardHandler)/server = HTTPServer(('127.0.0.1', PORT), DashboardHandler)/g" /opt/nut-dashboard/dashboard.py
systemctl restart nut-dashboard.service

# 3. Install Nginx
echo "Installing Nginx..."
apt-get update && apt-get install -y nginx

# 4. Generate Self-Signed SSL Certificate
echo "Generating self-signed SSL certificate..."
mkdir -p /etc/ssl/private /etc/ssl/certs
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt \
  -subj "/CN=shoim-1.bavariaduo.home/O=BavariaDuo/OU=HomeServer"

# 5. Create Nginx Configuration
echo "Configuring Nginx reverse proxy..."
cat << 'EOF' > /etc/nginx/sites-available/nut-dashboard
server {
    listen 80;
    listen [::]:80;
    server_name shoim-1.bavariaduo.home shoim-1;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name shoim-1.bavariaduo.home shoim-1;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable configuration and disable default site
ln -sf /etc/nginx/sites-available/nut-dashboard /etc/nginx/sites-enabled/nut-dashboard
rm -f /etc/nginx/sites-enabled/default

# Restart Nginx
systemctl restart nginx

echo "All tasks completed successfully!"
