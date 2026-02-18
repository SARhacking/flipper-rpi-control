"""
Configuration management for Flipper RPi Control
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class Config:
    """Configuration handler for the application"""

    DEFAULT_CONFIG_PATH = os.path.expanduser("~/.flipper-rpi/config.yaml")
    DEFAULT_LOG_PATH = os.path.expanduser("~/.flipper-rpi/logs")

    def __init__(self, config_path: str = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config_dir = os.path.dirname(self.config_path)
        self.log_dir = self.DEFAULT_LOG_PATH
        
        # Create directories if they don't exist
        self._ensure_directories()
        
        # Default configuration
        self._defaults = {
            "flipper_url": "http://localhost:8080",
            "timeout": 10,
            "log_level": "INFO",
            "proxy_port": 8888,
            "enable_web_ui": True,
            "web_ui_port": 5000,
            "auto_start_proxy": False,
        }
        
        # Load configuration
        self.config = self._load_config()

    def _ensure_directories(self):
        """Ensure required directories exist"""
        Path(self.config_dir).mkdir(parents=True, exist_ok=True)
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = yaml.safe_load(f) or {}
                # Merge with defaults
                config = {**self._defaults, **loaded_config}
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
            except Exception as e:
                logger.error(f"Failed to load config: {e}. Using defaults.")
                return self._defaults
        else:
            # Create default config file
            self._save_config(self._defaults)
            return self._defaults

    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def __getattr__(self, name: str):
        """Allow accessing config values as attributes"""
        if name.startswith('_'):
            return super().__getattribute__(name)
        return self.config.get(name, self._defaults.get(name))

    def update(self, **kwargs):
        """Update configuration values"""
        self.config.update(kwargs)
        self._save_config(self.config)
        logger.info(f"Configuration updated: {kwargs}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary"""
        return self.config.copy()
