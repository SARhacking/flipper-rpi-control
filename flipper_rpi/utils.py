"""
Utility functions for Flipper RPi Control
"""

import logging
import json
from typing import Any, Dict
from datetime import datetime
from pathlib import Path
import psutil


def setup_logging(log_dir: str, log_level: str = "INFO"):
    """Setup logging for the application"""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    log_file = Path(log_dir) / f"flipper-rpi-{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def print_table(data: list[Dict[str, Any]], headers: list[str] = None):
    """Print data as a formatted table"""
    if not data:
        print("No data to display")
        return
    
    if headers is None:
        headers = list(data[0].keys())
    
    # Calculate column widths
    col_widths = {header: len(header) for header in headers}
    for row in data:
        for header in headers:
            col_widths[header] = max(col_widths[header], len(str(row.get(header, ""))))
    
    # Print header
    header_row = " | ".join(header.ljust(col_widths[header]) for header in headers)
    print(header_row)
    print("-" * len(header_row))
    
    # Print rows
    for row in data:
        print(" | ".join(str(row.get(header, "")).ljust(col_widths[header]) for header in headers))


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as JSON string"""
    return json.dumps(data, indent=indent, default=str)


def get_system_stats() -> Dict[str, Any]:
    """Get current system statistics"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total_gb": psutil.virtual_memory().total / (1024**3),
            "available_gb": psutil.virtual_memory().available / (1024**3),
            "percent": psutil.virtual_memory().percent,
        },
        "disk": {
            "total_gb": psutil.disk_usage("/").total / (1024**3),
            "free_gb": psutil.disk_usage("/").free / (1024**3),
            "percent": psutil.disk_usage("/").percent,
        }
    }


def validate_port(port: int) -> bool:
    """Validate if a port is available and valid"""
    if not 1 <= port <= 65535:
        return False
    
    # Check if port is in use
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return False
    
    return True


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} PB"


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def colored_text(text: str, color: str) -> str:
    """Return colored text for terminal output"""
    return f"{color}{text}{Colors.RESET}"


def success_message(message: str) -> str:
    """Format a success message"""
    return colored_text(f"✓ {message}", Colors.GREEN)


def error_message(message: str) -> str:
    """Format an error message"""
    return colored_text(f"✗ {message}", Colors.RED)


def info_message(message: str) -> str:
    """Format an info message"""
    return colored_text(f"ℹ {message}", Colors.BLUE)


def warning_message(message: str) -> str:
    """Format a warning message"""
    return colored_text(f"⚠ {message}", Colors.YELLOW)
