sudo su


# GITHUB
ssh-keygen -t rsa -b 4096 -C "tejasteyn@example.com"
cat ~/.ssh/id_rsa.pub  # add this to github SSH keys
git clone git@github.com:Teja-Sureddy/django-documentation.git


# DOCKER
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo apt install docker-compose
docker-compose --version
sudo gpasswd -a $USER docker
newgrp docker


# RUN
cd ~/django-documentation
docker-compose -f docker-compose.prod.yml up -d --build
# docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml exec django python manage.py add_users
docker-compose -f docker-compose.prod.yml exec django python manage.py add_data
docker-compose -f docker-compose.prod.yml exec django python manage.py add_notifications
docker-compose -f docker-compose.prod.yml exec django python manage.py add_invoices


# CERTBOT
docker-compose -f docker-compose.prod.yml up --force-recreate -d nginx
docker-compose -f docker-compose.prod.yml run --rm --entrypoint "rm -Rf /etc/letsencrypt/live/django.tejasureddy.com && rm -Rf /etc/letsencrypt/archive/django.tejasureddy.com && rm -Rf /etc/letsencrypt/renewal/django.tejasureddy.com.conf" certbot
docker-compose -f docker-compose.prod.yml run --rm --entrypoint "certbot certonly --webroot -w /var/www/certbot --email tejasteyn@gmail.com -d django.tejasureddy.com --rsa-key-size 4096 --agree-tos --force-renewal" certbot
# uncomment 443 from nginx/nginx.conf
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload

# if error
# sudo chmod -R 755 /home/ubuntu/django-documentation/certbot/conf/live
# sudo chown -R www-data:www-data /home/ubuntu/django-documentation/certbot/conf/live


# RENEW CERTBOT
docker-compose run --rm certbot renew
