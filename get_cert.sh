#!/bin/bash
set -e

# 1. Update hostname of the system to shoim-1.bavariaduo.ovh
echo "Updating system hostname to shoim-1.bavariaduo.ovh..."
hostnamectl set-hostname shoim-1.bavariaduo.ovh

# Update /etc/hosts
sed -i 's/127.0.1.1.*/127.0.1.1\tshoim-1.bavariaduo.ovh shoim-1/g' /etc/hosts
sed -i 's/localhost shoim-1.bavariaduo.home/localhost shoim-1.bavariaduo.ovh/g' /etc/hosts

# 2. Install Certbot and OVH DNS plugin
echo "Installing Certbot and OVH DNS plugin..."
apt-get update && apt-get install -y certbot python3-certbot-dns-ovh

# 3. Create the OVH credentials configuration
echo "Writing OVH credentials configuration..."
mkdir -p /etc/letsencrypt
cat << 'EOF' > /etc/letsencrypt/ovh.ini
dns_ovh_endpoint = ovh-eu
dns_ovh_application_key = 
dns_ovh_application_secret = 
dns_ovh_consumer_key = 
EOF

chmod 600 /etc/letsencrypt/ovh.ini

# 4. Request the certificate from Let's Encrypt using DNS challenge
echo "Requesting certificate from Let's Encrypt..."
certbot certonly \
  --dns-ovh \
  --dns-ovh-credentials /etc/letsencrypt/ovh.ini \
  --dns-ovh-propagation-seconds 60 \
  -d shoim-1.bavariaduo.ovh \
  --non-interactive \
  --agree-tos \
  --email sieraindiagolf@gmail.com

# 5. Update Nginx configuration to use the new certificate
echo "Updating Nginx configuration to use the new Let's Encrypt certificate..."
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

    ssl_certificate /etc/letsencrypt/live/shoim-1.bavariaduo.ovh/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/shoim-1.bavariaduo.ovh/privkey.pem;

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
