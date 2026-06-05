#!/bin/bash
set -e

# 1. Update hostname of the system to shoim-1.bavariaduo.ovh
echo "Updating system hostname to shoim-1.bavariaduo.ovh..."
hostnamectl set-hostname shoim-1.bavariaduo.ovh

# Update /etc/hosts
sed -i 's/127.0.1.1.*/127.0.1.1\tshoim-1.bavariaduo.ovh shoim-1/g' /etc/hosts
sed -i 's/localhost shoim-1.bavariaduo.home/localhost shoim-1.bavariaduo.ovh/g' /etc/hosts

# 2. Install acme.sh client
echo "Installing acme.sh..."
curl https://get.acme.sh | sh -s email=sieraindiagolf@gmail.com
# Load acme.sh alias into current session
. "$HOME/.acme.sh/acme.sh.env" || true
export PATH="$HOME/.acme.sh:$PATH"

# 3. Request the certificate from Let's Encrypt using OVH DNS challenge
echo "Requesting SSL certificate via acme.sh..."
export OVH_AK=""
export OVH_AS=""
export OVH_CK=""

# Issue certificate (Let's Encrypt is the default now or we specify --server letsencrypt)
~/.acme.sh/acme.sh --issue --server letsencrypt --dns dns_ovh -d shoim-1.bavariaduo.ovh

# 4. Install certificate and configure auto-reload of Nginx
echo "Installing certificate to Nginx directory..."
mkdir -p /etc/nginx/ssl
~/.acme.sh/acme.sh --install-cert -d shoim-1.bavariaduo.ovh \
  --key-file       /etc/nginx/ssl/shoim-1.bavariaduo.ovh.key \
  --fullchain-file /etc/nginx/ssl/shoim-1.bavariaduo.ovh.pem \
  --reloadcmd     "systemctl reload nginx"

# 5. Update Nginx configuration to use the new certificate
echo "Updating Nginx configuration..."
cat << 'EOF' > /etc/nginx/sites-available/nut-dashboard
server {
    listen 80;
    listen [::]:80;
    server_name shoim-1.bavariaduo.ovh shoim-1;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name shoim-1.bavariaduo.ovh shoim-1;

    ssl_certificate /etc/nginx/ssl/shoim-1.bavariaduo.ovh.pem;
    ssl_certificate_key /etc/nginx/ssl/shoim-1.bavariaduo.ovh.key;

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

# Restart Nginx to apply changes
nginx -t
systemctl restart nginx

echo "Certificate successfully installed and Nginx reloaded!"
