# Flipper RPi Control 🔒

A comprehensive Kali Linux application for FlipperHTTP integration and management. This tool allows you to run Kali Linux and use FlipperHTTP functionality simultaneously without interference.

## Features

✨ **Core Features:**
- 🌐 HTTP Proxy Interception - Intercept and analyze HTTP/HTTPS traffic
- 🎮 Request Manipulation - Modify requests on-the-fly before forwarding
- 📊 Real-time Monitoring - Monitor proxy status and system statistics
- ⚙️ Flexible Configuration - YAML-based configuration management
- 🖥️ Dual Interface - Both CLI and Web UI available
- 📝 Comprehensive Logging - Detailed logs for debugging and auditing
- 🔗 Device Integration - Seamless FlipperHTTP device integration
- 🖥️ System-Aware - Coexists with Kali Linux without conflicts

## Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/SARhacking/flipper-rpi-control
cd flipper-rpi-control
chmod +x install.sh
./install.sh
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/SARhacking/flipper-rpi-control
cd flipper-rpi-control

# Install Python dependencies
pip3 install -r requirements.txt

# Install the application
pip3 install -e .
```

### Requirements

- **OS:** Kali Linux (or any Debian-based Linux)
- **Python:** 3.8 or higher
- **Dependencies:** See `requirements.txt`

## Usage

### Command Line Interface

The application provides a powerful CLI with multiple commands:

```bash
# Show help
flipper-rpi --help

# Test connection to FlipperHTTP
flipper-rpi connect

# Start the HTTP proxy
flipper-rpi start-proxy --port 8888

# Stop the HTTP proxy
flipper-rpi stop-proxy

# Show proxy and system status
flipper-rpi status

# Get intercepted requests
flipper-rpi requests --limit 20

# Forward an intercepted request
flipper-rpi forward --request-id <ID> --body <modified_body>

# Show current configuration
flipper-rpi config-show

# Update configuration
flipper-rpi config-set --key proxy_port --value 9999

# Initialize application
flipper-rpi init
```

### Web Interface

Launch the interactive web dashboard:

```bash
# Start web server (default: localhost:5000)
flipper-rpi-web

# Start with custom host/port
flipper-rpi-web --host 0.0.0.0 --port 5000

# Enable debug mode
flipper-rpi-web --debug
```

Then open your browser to: `http://localhost:5000`

The web UI provides:
- Real-time proxy status monitoring
- System statistics (CPU, Memory, Disk)
- Interactive request list
- One-click proxy start/stop
- Configuration management

### Configuration

Configuration is stored in: `~/.flipper-rpi/config.yaml`

Default configuration:
```yaml
flipper_url: http://localhost:8080
timeout: 10
log_level: INFO
proxy_port: 8888
enable_web_ui: true
web_ui_port: 5000
auto_start_proxy: false
```

Edit the configuration file directly or use the CLI:
```bash
flipper-rpi config-set --key proxy_port --value 9999
flipper-rpi config-set --key log_level --value DEBUG
flipper-rpi config-set --key auto_start_proxy --value true
```

## Architecture

The application is structured in modules:

```
flipper_rpi/
├── __init__.py          # Package initialization
├── core.py              # FlipperHTTP client wrapper
├── config.py            # Configuration management
├── utils.py             # Utility functions
├── cli.py               # Command-line interface
├── web.py               # Web UI server
└── templates/
    └── dashboard.html   # Web dashboard
```

### Core Modules

- **core.py**: FlipperHTTPClient class that handles all communication with the FlipperHTTP service
- **config.py**: Configuration loader and manager using YAML files
- **utils.py**: Helper functions for logging, formatting, and system monitoring
- **cli.py**: Click-based CLI with multiple commands
- **web.py**: Flask web server with REST API and dashboard

## API Reference

### REST API Endpoints

When using the web server, the following endpoints are available:

```
GET  /api/health              - Health check
GET  /api/proxy/status        - Get proxy status
POST /api/proxy/start         - Start proxy (body: {port: 8888})
POST /api/proxy/stop          - Stop proxy
GET  /api/requests            - Get intercepted requests
POST /api/requests/forward    - Forward request
GET  /api/system/info         - Get system information
GET  /api/system/stats        - Get system statistics
GET  /api/config              - Get configuration
POST /api/config              - Update configuration
```

### Python API

Use the library in your own Python scripts:

```python
from flipper_rpi.config import Config
from flipper_rpi.core import FlipperHTTPClient

# Initialize configuration
config = Config()

# Create client
client = FlipperHTTPClient(config)

# Test connection
if client.connect():
    print("Connected!")

# Start proxy
result = client.start_proxy(port=8888)

# Get intercepted requests
requests = client.get_intercepted_requests(limit=10)

# Forward a request
client.forward_request("request_id_123", modified_body="new body")
```

## Project Structure

```
flipper-rpi-control/
├── flipper_rpi/              # Main package
│   ├── __init__.py
│   ├── core.py              # Core client functionality
│   ├── config.py            # Configuration management
│   ├── utils.py             # Utility functions
│   ├── cli.py               # CLI interface
│   ├── web.py               # Web server
│   └── templates/           # HTML templates
│       └── dashboard.html
├── setup.py                 # Package setup script
├── requirements.txt         # Python dependencies
├── install.sh              # Installation script
└── README.md               # This file
```

## Configuration Files

### Main Configuration: ~/.flipper-rpi/config.yaml

```yaml
# FlipperHTTP connection settings
flipper_url: http://localhost:8080
timeout: 10

# Logging settings
log_level: INFO

# Proxy settings
proxy_port: 8888
auto_start_proxy: false

# Web UI settings
enable_web_ui: true
web_ui_port: 5000
```

### Logs

Logs are stored in: `~/.flipper-rpi/logs/`

Daily log files are created with format: `flipper-rpi-YYYYMMDD.log`

## Troubleshooting

### Connection Issues

If you get connection errors:

1. Check if FlipperHTTP service is running:
   ```bash
   flipper-rpi connect
   ```

2. Verify the configuration:
   ```bash
   flipper-rpi config-show
   ```

3. Check logs:
   ```bash
   tail -f ~/.flipper-rpi/logs/*
   ```

### Port Already in Use

If the proxy port is already in use:

```bash
# Check what's using the port
lsof -i :8888

# Use a different port
flipper-rpi start-proxy --port 9999
```

### Permission Denied

If you get permission errors:

```bash
# Ensure proper permissions
chmod +x ~/.flipper-rpi/

# Reinstall with proper permissions
pip3 install -e . --user
```

## Development

### Setting up development environment

```bash
# Clone and navigate to repo
git clone https://github.com/SARhacking/flipper-rpi-control
cd flipper-rpi-control

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip3 install -e ".[dev]"
```

### Running tests

```bash
pytest tests/
```

### Code style

```bash
# Format code
black flipper_rpi/

# Check linting
flake8 flipper_rpi/
```

## Security Considerations

⚠️ **Important:**

1. **Network Access**: By default, the web UI binds to localhost. To access remotely, be careful about exposing it:
   ```bash
   # DON'T do this in untrusted networks:
   flipper-rpi-web --host 0.0.0.0
   ```

2. **Configuration Files**: The config file contains sensitive settings. Keep it secure:
   ```bash
   chmod 600 ~/.flipper-rpi/config.yaml
   ```

3. **Logs**: Logs may contain sensitive data. Rotate logs regularly:
   ```bash
   rm ~/.flipper-rpi/logs/*
   ```

## Performance Tips

1. **Limit Interception**: Don't intercept all traffic if unnecessary
2. **Regular Cleanup**: Clear old logs periodically
3. **Resource Monitoring**: Monitor system stats while proxy is running
4. **Port Selection**: Use higher ports (>1024) to avoid requiring root

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

MIT License - See LICENSE file for details

## Author

Security Researcher - SARhacking

## Support

For issues, questions, or feedback:
- Open an issue on GitHub
- Check existing documentation
- Review logs in `~/.flipper-rpi/logs/`

## Changelog

### v1.0.0 (2026-02-18)
- Initial release
- CLI interface with core commands
- Web UI with dashboard
- Configuration management
- System monitoring
- FlipperHTTP integration

## References

- [Kali Linux Documentation](https://www.kali.org/docs/)
- [FlipperHTTP](https://github.com/flipperdevices/flipper-http)
- [Python Click Documentation](https://click.palletsprojects.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

Made with ❤️ for the Kali Linux community
