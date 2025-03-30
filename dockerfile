FROM python:3.13-slim


WORKDIR /app

RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY PKDD/ ./PKDD/
COPY csv/ ./csv/
COPY init.sql app.py create_db_app.py requirements.txt \
gunicorn.sh nginx.conf ./

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_ENV=production

RUN sed -i 's/\r$//' gunicorn.sh && \
    chmod +x gunicorn.sh

CMD ["/bin/bash", "./gunicorn.sh"]