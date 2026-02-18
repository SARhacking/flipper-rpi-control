# Quick Start Guide - Flipper RPi Control

Get up and running with Flipper RPi Control in 5 minutes!

## Installation (30 seconds)

```bash
# Clone the repository
git clone https://github.com/SARhacking/flipper-rpi-control
cd flipper-rpi-control

# Run the installer
chmod +x install.sh
./install.sh
```

That's it! The installer will handle dependencies and setup.

## First Run

### 1. Check Connection

```bash
flipper-rpi connect
```

You should see: ✓ Connected to FlipperHTTP successfully

### 2. Start Your First Proxy

```bash
flipper-rpi start-proxy --port 8888
```

Output:
```
✓ Proxy started on port 8888
ℹ Configure your tools to use: localhost:8888
```

### 3. Use the Web Dashboard (Optional)

In another terminal:

```bash
flipper-rpi-web --host localhost --port 5000
```

Open browser to: `http://localhost:5000`

You'll see:
- Real-time proxy status
- System statistics
- Intercepted requests
- Control buttons to start/stop proxy

## Common Tasks

### View Current Status

```bash
flipper-rpi status
```

Shows adapter status, system info, and statistics.

### List Intercepted Requests

```bash
flipper-rpi requests --limit 10
```

Shows the last 10 intercepted HTTP requests with methods and URLs.

### Stop Proxy

```bash
flipper-rpi stop-proxy
```

### Check Configuration

```bash
flipper-rpi config-show
```

### Change Proxy Port

```bash
flipper-rpi config-set --key proxy_port --value 9999
```

## Using with Kali Tools

Configure your tool to use the proxy:

**For Burp Suite:**
1. User Options → Network → Connections
2. Proxy → Proxy service
3. Set to: `127.0.0.1:8888`

**For curl:**
```bash
curl -x http://127.0.0.1:8888 https://example.com
```

**For Firefox:**
1. Preferences → Network → Manual proxy configuration
2. HTTP Proxy: `127.0.0.1`
3. Port: `8888`

**For Python requests:**
```python
import requests
proxies = {
    'http': 'http://127.0.0.1:8888',
    'https': 'http://127.0.0.1:8888',
}
requests.get('https://example.com', proxies=proxies)
```

## Troubleshooting

### "Can't connect to FlipperHTTP"

1. Check if service is running:
```bash
flipper-rpi connect
```

2. Verify configuration:
```bash
flipper-rpi config-show
```

3. Check the URL in config matches your FlipperHTTP instance

### "Port already in use"

```bash
# Use a different port
flipper-rpi start-proxy --port 9999

# Or kill the process using the port
lsof -i :8888
kill -9 <PID>
```

### "Permission denied"

```bash
# Fix permissions
chmod +x ~/.flipper-rpi/
pip3 install -e . --user
```

## Next Steps

- Read the full [README.md](README.md) for advanced features
- Check the [API Reference](README.md#api-reference) for integrations
- Join the community for support

## Tips

💡 **Pro Tips:**
- Use `--help` on any command for options
- Enable debug logging: `flipper-rpi --log-level DEBUG status`
- Web UI auto-refreshes every few seconds
- Logs are in `~/.flipper-rpi/logs/`
- Configuration is in `~/.flipper-rpi/config.yaml`

## Need Help?

- Check full documentation: [README.md](README.md)
- View logs: `tail -f ~/.flipper-rpi/logs/*`
- Reset config: `rm ~/.flipper-rpi/config.yaml` (will recreate with defaults)

---

Happy hacking! 🚀
