#!/bin/sh

if [ "$PROJECT_SERVICE_TYPE" = "api" ];
 then
    echo ">>> Copying Environment Credentials"
    cp env.credentials .env
    echo ">>> Collect Static Files"
    python manage.py collectstatic --noinput -v 0
    echo ">>> Running Migrations"
    python manage.py makemigrations
    echo ">>> Run Migration"
    python manage.py migrate -v 0
    echo ">>> Starting Gunicorn"
    gunicorn core.wsgi -b 0.0.0.0:80 --threads=8 --workers=4 --log-level=info
fi

if [ "$PROJECT_SERVICE_TYPE" = "worker" ];
 then
  echo ">>> Starting Celery Worker"
  celery --app core worker --loglevel=DEBUG
fi