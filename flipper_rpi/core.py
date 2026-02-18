"""
Core FlipperHTTP functionality wrapper
"""

import requests
import logging
from typing import Optional, Dict, Any
from .config import Config

logger = logging.getLogger(__name__)


class FlipperHTTPClient:
    """Main client for interacting with FlipperHTTP"""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.base_url = config.flipper_url
        self.timeout = config.timeout

    def connect(self) -> bool:
        """Test connection to FlipperHTTP"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/health",
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def start_proxy(self, port: int = 8080) -> Dict[str, Any]:
        """Start the HTTP proxy on specified port"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/proxy/start",
                json={"port": port},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to start proxy: {e}")
            return {"status": "error", "message": str(e)}

    def stop_proxy(self) -> Dict[str, Any]:
        """Stop the HTTP proxy"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/proxy/stop",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to stop proxy: {e}")
            return {"status": "error", "message": str(e)}

    def get_proxy_status(self) -> Dict[str, Any]:
        """Get current proxy status"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/proxy/status",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get proxy status: {e}")
            return {"status": "error", "message": str(e)}

    def get_intercepted_requests(self, limit: int = 50) -> Dict[str, Any]:
        """Get list of intercepted requests"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/requests",
                params={"limit": limit},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get requests: {e}")
            return {"status": "error", "message": str(e)}

    def forward_request(self, request_id: str, modified_body: Optional[str] = None) -> Dict[str, Any]:
        """Forward an intercepted request"""
        try:
            payload = {"request_id": request_id}
            if modified_body:
                payload["body"] = modified_body
            response = self.session.post(
                f"{self.base_url}/api/requests/forward",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to forward request: {e}")
            return {"status": "error", "message": str(e)}

    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/system/info",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return {"status": "error", "message": str(e)}

    def set_proxy_rules(self, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Set proxy filtering and forwarding rules"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/proxy/rules",
                json=rules,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to set proxy rules: {e}")
            return {"status": "error", "message": str(e)}
