#!/bin/bash
# Uruchom skrypt tworzący bazę danych
python /app/create_db_app.py

# Uruchom Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:8000 app:app