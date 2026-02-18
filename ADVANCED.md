# Advanced Configuration Guide

## Environment Variables

Configure Flipper RPi Control using environment variables:

```bash
# FlipperHTTP connection
export FLIPPER_URL="http://192.168.1.100:8080"
export FLIPPER_TIMEOUT="15"

# Proxy settings
export PROXY_PORT="9000"
export AUTO_START_PROXY="true"

# Web UI
export ENABLE_WEB_UI="true"
export WEB_UI_PORT="3000"
export WEB_UI_HOST="0.0.0.0"

# Logging
export LOG_LEVEL="DEBUG"

# Then run the application
flipper-rpi status
```

## Configuration File (YAML)

Edit `~/.flipper-rpi/config.yaml`:

```yaml
# Connection Configuration
flipper_url: http://localhost:8080
timeout: 10

# Proxy Configuration
proxy_port: 8888
auto_start_proxy: false

# Web UI Configuration
enable_web_ui: true
web_ui_port: 5000
web_ui_host: "127.0.0.1"

# Logging Configuration
log_level: INFO  # DEBUG, INFO, WARNING, ERROR

# Advanced Options
request_history_limit: 1000
enable_ssl_bypass: false
max_concurrent_requests: 100
```

## Multiple Ports Setup

Run multiple proxy instances on different ports for different tools:

```bash
# Terminal 1: Proxy for Burp Suite
flipper-rpi config-set --key proxy_port --value 8888
flipper-rpi start-proxy --port 8888

# Terminal 2: Proxy for curl/wget
flipper-rpi config-set --key proxy_port --value 8889
flipper-rpi start-proxy --port 8889

# Terminal 3: Web UI
flipper-rpi-web --port 5000
```

## Kali Linux Integration

### Add to Kali Tools Menu

Create `/usr/share/applications/flipper-rpi.desktop`:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Flipper RPi Control
Comment=FlipperHTTP management tool
Exec=gnome-terminal -- flipper-rpi-web --host 0.0.0.0 --port 5000
Icon=network-proxy
Categories=System;SecurityTools;
X-Kali-Package=flipper-rpi-control
```

Then run:
```bash
sudo update-desktop-database
```

### Add to PATH

If not installed via pip:
```bash
export PATH="/opt/flipper-rpi-control:$PATH"
```

## Docker Deployment

### Build Custom Image

```bash
docker build -t flipper-rpi:latest .
```

### Run Container

```bash
# Simple run
docker run -it -p 5000:5000 -p 8888:8888 flipper-rpi:latest

# With volume mounts
docker run -it \
  -p 5000:5000 \
  -p 8888:8888 \
  -v ~/.flipper-rpi:/root/.flipper-rpi \
  flipper-rpi:latest

# Run web UI
docker run -it \
  -p 5000:5000 \
  -p 8888:8888 \
  flipper-rpi:latest \
  flipper-rpi-web --host 0.0.0.0
```

### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f flipper-rpi-control

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v
```

## Network Configuration

### Access Web UI Remotely

**WARNING:** Only do this in secure networks!

```bash
flipper-rpi-web --host 0.0.0.0 --port 5000
```

### Reverse Proxy Setup (nginx)

```nginx
server {
    listen 80;
    server_name flipper.example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /api {
        proxy_pass http://localhost:5000/api;
        proxy_set_header Host $host;
    }
}
```

Enable: `sudo systemctl restart nginx`

## Performance Tuning

### Handle Large Traffic Volumes

```yaml
# config.yaml
request_history_limit: 5000
enable_compression: true
buffer_size: 65536
thread_pool_size: 10
```

### Memory Optimization

```bash
# Run with memory limit
flipper-rpi-web --flask-debug False
```

### CPU Optimization

```bash
# Single threaded (low CPU)
flipper-rpi-web --threaded False
```

## Security Hardening

### Disable Web UI

```yaml
enable_web_ui: false
```

### Restrict Ports

```bash
# Use high port numbers
flipper-rpi config-set --key proxy_port --value 8000
```

### Enable HTTPS for Web UI

```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Configure (future version)
# flipper-rpi-web --ssl-cert cert.pem --ssl-key key.pem
```

### Firewall Rules

```bash
# Allow only localhost
sudo ufw allow from 127.0.0.1 to any port 5000
sudo ufw allow from 127.0.0.1 to any port 8888

# Allow from specific IP
sudo ufw allow from 192.168.1.100 to any port 5000
```

## Logging Configuration

### Change Log Level

```bash
# At runtime
flipper-rpi --log-level DEBUG status

# In config
flipper-rpi config-set --key log_level --value DEBUG
```

### Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/flipper-rpi
```

```
/root/.flipper-rpi/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 root root
}
```

Enable: `sudo logrotate -f /etc/logrotate.d/flipper-rpi`

## Systemd Service

Create `/etc/systemd/system/flipper-rpi-web.service`:

```ini
[Unit]
Description=Flipper RPi Control Web UI
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/flipper-rpi-web --host 0.0.0.0 --port 5000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable: `sudo systemctl enable flipper-rpi-web`
Start: `sudo systemctl start flipper-rpi-web`

## Integration Examples

### With Burp Suite

```bash
# Start proxy
flipper-rpi start-proxy --port 8888

# Then in Burp:
# Proxy → Options → Proxy Listeners
# Add: Address 127.0.0.1:8888
```

### With OWASP ZAP

```bash
# Start Flipper proxy
flipper-rpi start-proxy --port 8888

# ZAP Settings > Network > Connection Options
# Use upstream proxy: localhost:8888
```

### With Python Scripts

```python
from flipper_rpi.config import Config
from flipper_rpi.core import FlipperHTTPClient

config = Config(config_path="/custom/path/config.yaml")
client = FlipperHTTPClient(config)

# Use custom timeouts
config.update(timeout=30)

# Get requests with filters
requests = client.get_intercepted_requests(limit=100)
```

## Troubleshooting Configuration

### Reset to Defaults

```bash
rm ~/.flipper-rpi/config.yaml
flipper-rpi init
```

### Verify Configuration

```bash
flipper-rpi config-show
# Displays all current settings
```

### Check Active Connections

```bash
netstat -tlnp | grep flipper
lsof -i :8888
```

### Debug Mode

```bash
# Run with debug output
FLASK_DEBUG=1 flipper-rpi-web

# Or
flipper-rpi --log-level DEBUG start-proxy --port 8888
```

---

For more help, see the main [README.md](README.md)
