#!/bin/bash

# Create virtualenv (venv)
python3 -m venv venv
# Activate virtual environment
source venv/bin/activate
# Upgrade pip
pip install --upgrade pip
# Install using requirements.txt
pip install -r requirements.txt
# Virtual environment remains activated after installation
echo "Virtualenv venv is activated."
# cd to project directory
cd d09
# db migration
python manage.py makemigrations
python manage.py migrate
# translation
#python manage.py makemessages -l en
#python manage.py makemessages -l ja
#python manage.py compilemessages
# test
#python manage.py test
# run server
python manage.py runserver


## initial data creation
#python manage.py loaddata initial_data
#cd myproject && python manage.py createsuperuser --username john_doe --email john@example.com
