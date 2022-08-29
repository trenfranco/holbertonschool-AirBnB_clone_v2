#!/usr/bin/env bash
#script that sets up your web servers for the deployment of web_static

apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
echo "Test" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu /data/
chgrp -R ubuntu /data/
sed -i "/listen 80 default_server/a \\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

service nginx restart
