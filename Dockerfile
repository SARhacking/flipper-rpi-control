FROM kalilinux/kali-rolling

LABEL maintainer="SARhacking" \
      description="Flipper RPi Control - Kali Linux FlipperHTTP Management Tool" \
      version="1.0.0"

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/flipper-rpi-control

# Copy application files
COPY . .

# Install application
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir -e .

# Create config directory
RUN mkdir -p /root/.flipper-rpi/logs

# Expose ports
EXPOSE 5000 8888

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO

# Default command: show help
CMD ["flipper-rpi", "--help"]
