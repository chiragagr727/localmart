# Backend Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app

# Create logs dir to match settings.py
RUN mkdir -p /app/logs /app/staticfiles /app/media

ENV DJANGO_SETTINGS_MODULE=local_delivery.settings

CMD ["sh", "-c", "python manage.py makemigrations apps.users apps.shops apps.products apps.orders apps.payments apps.feedback apps.notifications && python manage.py migrate && python manage.py collectstatic --noinput && daphne -b 0.0.0.0 -p 8000 local_delivery.asgi:application"]
