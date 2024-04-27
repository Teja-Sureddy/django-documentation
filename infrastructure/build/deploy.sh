sudo su
cd django-documentation
git reset --hard HEAD
git switch main
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build django
