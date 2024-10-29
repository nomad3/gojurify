# n8n/Dockerfile

FROM n8nio/n8n:latest

# Set environment variables (these should be overridden in docker-compose using .env)
ENV N8N_BASIC_AUTH_ACTIVE=${N8N_BASIC_AUTH_ACTIVE}
ENV N8N_BASIC_AUTH_USER=${N8N_BASIC_AUTH_USER}
ENV N8N_BASIC_AUTH_PASSWORD=${N8N_BASIC_AUTH_PASSWORD}
ENV N8N_HOST=${N8N_HOST}
ENV N8N_PORT=${N8N_PORT}
ENV WEBHOOK_URL=${WEBHOOK_URL}
ENV N8N_PROTOCOL=${N8N_PROTOCOL}

# Expose the n8n port
EXPOSE ${N8N_PORT}

# Define a volume for n8n data persistence
VOLUME ["/root/.n8n"]
