"""
Flipper RPi Control - Kali Linux application for FlipperHTTP management
"""

__version__ = "1.0.0"
__author__ = "Security Researcher"

from . import core
from . import utils
from . import config

__all__ = ["core", "utils", "config"]
