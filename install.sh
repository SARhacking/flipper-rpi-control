#!/bin/bash
# Installation script for Flipper RPi Control on Kali Linux

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║  Flipper RPi Control - Kali Linux Installation Script  ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    SUDO=""
else 
    SUDO="sudo"
fi

# Detect package manager
if command -v apt-get &> /dev/null; then
    PKG_MGR="apt-get"
elif command -v dnf &> /dev/null; then
    PKG_MGR="dnf"
else
    echo "❌ Unsupported package manager"
    exit 1
fi

echo "📦 Installing system dependencies..."
$SUDO $PKG_MGR update
$SUDO $PKG_MGR install -y python3 python3-pip python3-venv

echo "📁 Ensuring required directories exist..."
mkdir -p ~/.flipper-rpi/logs

echo "📚 Installing Python dependencies..."
pip3 install --upgrade pip setuptools wheel

echo "🔧 Installing Flipper RPi Control..."
pip3 install -e .

echo "✅ Installation complete!"
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  Getting Started                                       ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Command-line interface:"
echo "  $ flipper-rpi --help           # Show help"
echo "  $ flipper-rpi connect          # Test connection"
echo "  $ flipper-rpi start-proxy      # Start proxy server"
echo "  $ flipper-rpi status           # Show status"
echo "  $ flipper-rpi config-show      # Show configuration"
echo ""
echo "Web interface:"
echo "  $ flipper-rpi-web --port 5000 --host 0.0.0.0"
echo "  Then open: http://localhost:5000"
echo ""
echo "Configuration file:"
echo "  ~/.flipper-rpi/config.yaml"
echo ""
echo "For more information, run: flipper-rpi --help"
echo ""
