
@echo off
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
if not exist .env copy .env.sample .env
python manage.py migrate
python manage.py runserver
