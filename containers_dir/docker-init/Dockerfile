FROM python:3.13-slim

WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy only necessary files for database initialization
COPY PKDD/ ./PKDD/
COPY csv/ ./csv/
COPY init.sql app.py create_db_app.py requirements.txt \
 nginx.conf .env ./


ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "create_db_app.py"]
