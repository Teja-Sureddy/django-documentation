sudo su
cd django-documentation
git reset --hard HEAD
git switch buildspec
git pull origin buildspec
docker-compose -f docker-compose.prod.yml up -d --build django
