#! /bin/sh

python manage.py makemigrations
python manage.py migrate

python manage.py collectstatic --noinput

rm /tmp/*.pid

celery multi start 1 -c 4 -A futureproof -B -l info -Ofair --logfile=/code/logging/celery.log --pidfile=/tmp/%n.pid

gunicorn --access-logfile - --workers 4 --timeout 300 --reload \
  --bind web_app:8000 futureproof.wsgi:application