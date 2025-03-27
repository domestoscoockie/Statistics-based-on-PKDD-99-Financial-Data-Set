FROM python:3.13-slim


WORKDIR /app

RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY PKDD/ ./PKDD/
COPY csv/ ./csv/
COPY init.sql app.py create_db_app.py requirements.txt \
gunicorn.sh nginx.conf start.sh  ./

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_ENV=production

RUN chmod +x /app/gunicorn.sh

ENTRYPOINT ["/app/gunicorn.sh"]