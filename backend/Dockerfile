FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /code/logs /code/staticfiles /code/media \
    && chown -R app:app /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Set proper permissions
RUN chown -R app:app /code

# Switch to non-root user
USER app

# Collect static files
RUN mkdir -p /code/logs \
    && touch /code/logs/debug.log \
    && python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
