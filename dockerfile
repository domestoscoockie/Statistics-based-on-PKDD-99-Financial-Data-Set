FROM python:3.13-slim


WORKDIR /app

RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY PKDD/ ./PKDD/
COPY csv/ ./csv/
COPY app.py create_db_app.py requirements.txt ./

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_ENV=production

CMD ["/bin/bash", "-c", "tail -f /dev/null"]