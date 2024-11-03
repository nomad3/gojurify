# Use Python 3.9 slim image
FROM python:3.9-slim

# Add system user and group
RUN addgroup --system app && adduser --system --ingroup app app

# Set working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories and set permissions
RUN mkdir -p /code/logs /code/staticfiles /code/media \
    && chown -R app:app /code

# Copy requirements first to leverage Docker cache
COPY requirements.txt /code/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Set ownership of all files to app user
RUN chown -R app:app /code

# Create a default .env file if it doesn't exist
RUN echo "SECRET_KEY=django-insecure-default-development-key-change-this" > /code/.env

# Create logs directory and run collectstatic
RUN mkdir -p /code/logs \
    && touch /code/logs/debug.log \
    && python manage.py collectstatic --noinput

# Switch to non-root user
USER app

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "gojurify.wsgi:application"] 