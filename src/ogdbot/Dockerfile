FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FFMPEG_PATH=/usr/bin/ffmpeg \
    PYTHONFAULTHANDLER=1

WORKDIR /ocbot

# Install system dependencies using apk
RUN apk add --no-cache \
    ffmpeg \
    opus-dev \
    libffi-dev \
    gcc \
    musl-dev \
    python3-dev \
    py3-pip \
    && rm -rf /var/cache/apk/*  # Clean up apk cache to reduce image size

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user and set permissions
RUN mkdir -p /sounds/opus && \
    adduser -D botuser && \
    chown -R botuser:botuser /ocbot /sounds && \
    chmod -R 777 /sounds/opus  
# Ensure write permissions for /sounds/opus directory

USER botuser

# Make the script explicitly executable
RUN chmod +x main.py

# Command to run the bot
CMD ["python", "-u", "main.py"]