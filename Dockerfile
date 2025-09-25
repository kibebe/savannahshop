# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# system deps for common packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy app
COPY . /app

# collect static if you use it (nofail)
RUN python manage.py collectstatic --noinput || true

# default command (web); Celery in K8s will override the command
CMD ["gunicorn", "savannahshop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
