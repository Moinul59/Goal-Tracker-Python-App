FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Environment defaults (override via docker-compose or .env)
ENV FLASK_APP=app.py \
    PYTHONUNBUFFERED=1 

# Expose gunicorn port
EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Default command (overridden per service in docker-compse)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]