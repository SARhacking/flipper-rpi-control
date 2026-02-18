"""
Web UI for Flipper RPi Control
"""

from flask import Flask, render_template, jsonify, request
import logging
from .config import Config
from .core import FlipperHTTPClient
from .utils import get_system_stats


def create_app(config: Config = None):
    """Create Flask application"""
    
    if config is None:
        config = Config()
    
    app = Flask(__name__)
    client = FlipperHTTPClient(config)
    logger = logging.getLogger(__name__)
    
    # Store config and client in app context
    app.config['flipper_config'] = config
    app.config['flipper_client'] = client
    
    @app.route('/')
    def index():
        """Dashboard page"""
        return render_template('dashboard.html')
    
    @app.route('/api/health')
    def health():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "version": "1.0.0"})
    
    @app.route('/api/proxy/status')
    def proxy_status():
        """Get proxy status"""
        return jsonify(client.get_proxy_status())
    
    @app.route('/api/proxy/start', methods=['POST'])
    def start_proxy():
        """Start proxy"""
        data = request.get_json() or {}
        port = data.get('port', 8888)
        return jsonify(client.start_proxy(port=port))
    
    @app.route('/api/proxy/stop', methods=['POST'])
    def stop_proxy():
        """Stop proxy"""
        return jsonify(client.stop_proxy())
    
    @app.route('/api/requests')
    def get_requests():
        """Get intercepted requests"""
        limit = request.args.get('limit', 50, type=int)
        return jsonify(client.get_intercepted_requests(limit=limit))
    
    @app.route('/api/requests/forward', methods=['POST'])
    def forward_request():
        """Forward an intercepted request"""
        data = request.get_json() or {}
        request_id = data.get('request_id')
        modified_body = data.get('body')
        
        if not request_id:
            return jsonify({"status": "error", "message": "request_id required"}), 400
        
        return jsonify(client.forward_request(request_id, modified_body))
    
    @app.route('/api/system/info')
    def system_info():
        """Get system information"""
        return jsonify(client.get_system_info())
    
    @app.route('/api/system/stats')
    def system_stats():
        """Get local system statistics"""
        return jsonify(get_system_stats())
    
    @app.route('/api/config')
    def get_config():
        """Get current configuration"""
        return jsonify(config.to_dict())
    
    @app.route('/api/config', methods=['POST'])
    def set_config():
        """Update configuration"""
        data = request.get_json() or {}
        try:
            config.update(**data)
            return jsonify({"status": "success", "config": config.to_dict()})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    
    @app.errorhandler(404)
    def not_found(e):
        """404 error handler"""
        return jsonify({"status": "error", "message": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        """500 error handler"""
        logger.error(f"Server error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
    
    return app


def main():
    """Main entry point for web UI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Flipper RPi Control Web UI')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--config', help='Path to config file')
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config(config_path=args.config)
    
    # Create Flask app
    app = create_app(config)
    
    # Run app
    print(f"Starting Flipper RPi Control Web UI on http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
