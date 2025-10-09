FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apk add --no-cache \
    build-base \
    rust \
    cargo \
    python3-dev \
    curl \
    # Clean up the APK cache to reduce this stage's layer size
    && rm -rf /var/cache/apk/*

WORKDIR /src/app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies and curl for healthcheck
RUN apk add --no-cache curl && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

RUN chmod +x /src/app/entrypoint.sh

ENTRYPOINT ["/src/app/entrypoint.sh"]