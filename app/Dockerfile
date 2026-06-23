FROM python:3.12-slim

LABEL maintainer="Brandon Loh"
LABEL project="compose-nginx-flask-postgres"
LABEL description="Flask app running with Gunicorn behind Nginx using Docker Compose"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && adduser --disabled-password --gecos "" appuser

COPY app.py .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]