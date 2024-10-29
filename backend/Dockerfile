FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup --system app && adduser --system --ingroup app app

WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Change ownership to non-root user
RUN chown -R app:app /code

USER app

EXPOSE 8000

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
