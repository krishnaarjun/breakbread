#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata userdump.json
python manage.py loaddata howyouhear.json
python manage.py loaddata potlucksurveydump.json
python manage.py loaddata potluckfood.json
python manage.py runserver 0.0.0.0:8000