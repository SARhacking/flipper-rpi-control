"""
CLI interface for Flipper RPi Control
"""

import click
import logging
from .config import Config
from .core import FlipperHTTPClient
from .utils import (
    setup_logging, print_table, format_json, get_system_stats,
    success_message, error_message, info_message, warning_message,
    validate_port
)


# Define a group for the CLI
@click.group()
@click.option('--config', type=click.Path(), help='Path to config file')
@click.option('--log-level', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR']), 
              default='INFO', help='Logging level')
@click.pass_context
def cli(ctx, config, log_level):
    """Flipper RPi Control - Kali Linux tool for FlipperHTTP management"""
    
    # Load configuration
    cfg = Config(config_path=config)
    cfg.update(log_level=log_level)
    
    # Setup logging
    setup_logging(cfg.log_dir, log_level)
    
    # Store config in context
    ctx.ensure_object(dict)
    ctx.obj['config'] = cfg
    ctx.obj['client'] = FlipperHTTPClient(cfg)
    ctx.obj['logger'] = logging.getLogger(__name__)


@cli.command()
@click.pass_context
def connect(ctx):
    """Test connection to FlipperHTTP"""
    client = ctx.obj['client']
    logger = ctx.obj['logger']
    
    click.echo("Testing connection to FlipperHTTP...")
    
    if client.connect():
        click.echo(success_message("Connected to FlipperHTTP successfully"))
    else:
        click.echo(error_message("Failed to connect to FlipperHTTP"))
        logger.error("Connection test failed")


@cli.command()
@click.option('--port', type=int, default=8888, help='Proxy port (default: 8888)')
@click.pass_context
def start_proxy(ctx, port):
    """Start the HTTP proxy"""
    client = ctx.obj['client']
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    # Validate port
    if not validate_port(port):
        click.echo(error_message(f"Port {port} is not available or invalid"))
        return
    
    click.echo(f"Starting proxy on port {port}...")
    
    result = client.start_proxy(port=port)
    
    if result.get("status") == "success":
        config.update(proxy_port=port)
        click.echo(success_message(f"Proxy started on port {port}"))
        click.echo(info_message(f"Configure your tools to use: localhost:{port}"))
    else:
        click.echo(error_message(f"Failed to start proxy: {result.get('message')}"))
        logger.error(f"Proxy start failed: {result}")


@cli.command()
@click.pass_context
def stop_proxy(ctx):
    """Stop the HTTP proxy"""
    client = ctx.obj['client']
    logger = ctx.obj['logger']
    
    click.echo("Stopping proxy...")
    
    result = client.stop_proxy()
    
    if result.get("status") == "success":
        click.echo(success_message("Proxy stopped"))
    else:
        click.echo(error_message(f"Failed to stop proxy: {result.get('message')}"))


@cli.command()
@click.pass_context
def status(ctx):
    """Get proxy status and system information"""
    client = ctx.obj['client']
    logger = ctx.obj['logger']
    
    click.echo("Getting status...")
    
    # Get proxy status
    proxy_status = client.get_proxy_status()
    click.echo("\n" + click.style("Proxy Status:", fg="cyan", bold=True))
    click.echo(format_json(proxy_status))
    
    # Get system info
    sys_info = client.get_system_info()
    click.echo("\n" + click.style("System Information:", fg="cyan", bold=True))
    click.echo(format_json(sys_info))
    
    # Get local system stats
    local_stats = get_system_stats()
    click.echo("\n" + click.style("Local System Stats:", fg="cyan", bold=True))
    click.echo(format_json(local_stats))


@cli.command()
@click.option('--limit', type=int, default=10, help='Number of requests to show')
@click.pass_context
def requests(ctx, limit):
    """Show intercepted requests"""
    client = ctx.obj['client']
    logger = ctx.obj['logger']
    
    click.echo(f"Fetching last {limit} intercepted requests...")
    
    result = client.get_intercepted_requests(limit=limit)
    
    if result.get("status") == "success":
        requests_list = result.get("requests", [])
        if requests_list:
            # Simple table format
            click.echo("\n" + click.style("Intercepted Requests:", fg="cyan", bold=True))
            for i, req in enumerate(requests_list, 1):
                click.echo(f"\n[{i}] {req.get('method', 'UNKNOWN')} {req.get('url', 'N/A')}")
                click.echo(f"    Status: {req.get('status', 'pending')}")
                click.echo(f"    Size: {req.get('size', 'N/A')} bytes")
        else:
            click.echo(warning_message("No intercepted requests found"))
    else:
        click.echo(error_message(f"Failed to get requests: {result.get('message')}"))


@cli.command()
@click.option('--request-id', required=True, help='ID of the request to forward')
@click.option('--body', default=None, help='Modified request body (optional)')
@click.pass_context
def forward(ctx, request_id, body):
    """Forward an intercepted request"""
    client = ctx.obj['client']
    logger = ctx.obj['logger']
    
    click.echo(f"Forwarding request {request_id}...")
    
    result = client.forward_request(request_id, modified_body=body)
    
    if result.get("status") == "success":
        click.echo(success_message(f"Request forwarded successfully"))
    else:
        click.echo(error_message(f"Failed to forward request: {result.get('message')}"))


@cli.command()
@click.pass_context
def config_show(ctx):
    """Show current configuration"""
    config = ctx.obj['config']
    
    click.echo(click.style("Current Configuration:", fg="cyan", bold=True))
    click.echo(format_json(config.to_dict()))


@cli.command()
@click.option('--key', required=True, help='Configuration key')
@click.option('--value', required=True, help='Configuration value')
@click.pass_context
def config_set(ctx, key, value):
    """Set a configuration value"""
    config = ctx.obj['config']
    logger = ctx.obj['logger']
    
    # Try to parse value as different types
    try:
        if value.lower() in ('true', 'false'):
            parsed_value = value.lower() == 'true'
        elif value.isdigit():
            parsed_value = int(value)
        else:
            parsed_value = value
    except:
        parsed_value = value
    
    config.update(**{key: parsed_value})
    click.echo(success_message(f"Configuration updated: {key} = {parsed_value}"))
    logger.info(f"Config updated: {key} = {parsed_value}")


@cli.command()
@click.pass_context
def init(ctx):
    """Initialize or reset configuration"""
    config = ctx.obj['config']
    
    click.echo("Initializing configuration...")
    click.echo(f"Config directory: {config.config_dir}")
    click.echo(f"Config file: {config.config_path}")
    click.echo(f"Log directory: {config.log_dir}")
    
    click.echo(success_message("Initialization complete"))
    click.echo(info_message("Run 'flipper-rpi config-show' to view current settings"))


@cli.command()
def version():
    """Show version information"""
    import flipper_rpi
    click.echo(f"Flipper RPi Control v{flipper_rpi.__version__}")


def main():
    """Main entry point for CLI"""
    cli(obj={})


if __name__ == '__main__':
    main()
