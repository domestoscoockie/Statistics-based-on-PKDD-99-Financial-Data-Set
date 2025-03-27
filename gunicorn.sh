#!/bin/bash
python /app/create_db_app.py

exec gunicorn -c ./gunicorn.conf.py 'PKDD:create_app()'