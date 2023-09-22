#!/bin/sh

cd backend
python manage.py migrate --run-syncdb --no-input
python manage.py makemigrations images --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear
python seed.py
python manage.py runserver 0.0.0.0:8000