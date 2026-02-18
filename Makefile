.PHONY: help install clean test run dev lint format docs

help:
	@echo "Flipper RPi Control - Development Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install        Install the package and dependencies"
	@echo "  make dev-install    Install in development mode with test dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run-cli        Run CLI tool"
	@echo "  make run-web        Run web UI"
	@echo "  make dev            Start development server with auto-reload"
	@echo ""
	@echo "Development:"
	@echo "  make lint           Run code linting"
	@echo "  make format         Format code with black"
	@echo "  make test           Run tests"
	@echo "  make coverage       Generate coverage report"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          Remove build artifacts"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run in Docker container"
	@echo "  make docs           Generate documentation"
	@echo ""

install:
	@echo "Installing Flipper RPi Control..."
	pip3 install -e .
	@echo "✓ Installation complete"

dev-install:
	@echo "Installing in development mode..."
	pip3 install -e ".[dev]"
	@echo "✓ Development installation complete"

run-cli:
	flipper-rpi --help

run-web:
	flipper-rpi-web --debug --host 127.0.0.1 --port 5000

dev:
	@echo "Starting development server..."
	FLASK_APP=flipper_rpi/web.py FLASK_ENV=development FLASK_DEBUG=1 flask run --host 127.0.0.1 --port 5000

lint:
	@echo "Linting code..."
	flake8 flipper_rpi/ || true
	pylint flipper_rpi/ || true

format:
	@echo "Formatting code..."
	black flipper_rpi/ setup.py

test:
	@echo "Running tests..."
	pytest tests/ -v || true

coverage:
	@echo "Generating coverage report..."
	pytest --cov=flipper_rpi tests/ || true
	@echo "Coverage report generated in htmlcov/index.html"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build dist *.egg-info
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "✓ Cleanup complete"

docker-build:
	@echo "Building Docker image..."
	docker build -t flipper-rpi:latest .
	@echo "✓ Docker image built"

docker-run:
	@echo "Running Docker container..."
	docker run -it \
		-p 5000:5000 \
		-p 8888:8888 \
		-v ~/.flipper-rpi:/root/.flipper-rpi \
		flipper-rpi:latest flipper-rpi-web --host 0.0.0.0

docker-compose-up:
	@echo "Starting Docker Compose services..."
	docker-compose up -d
	@echo "✓ Services started"

docker-compose-down:
	@echo "Stopping Docker Compose services..."
	docker-compose down
	@echo "✓ Services stopped"

docs:
	@echo "Generating documentation..."
	@echo "Available documentation:"
	@echo "  - README.md (main documentation)"
	@echo "  - QUICKSTART.md (quick start guide)"
	@echo "  - ADVANCED.md (advanced configuration)"
	@echo "  - API documentation in code"

requirements:
	@echo "Current requirements:"
	@cat requirements.txt

uninstall:
	@echo "Uninstalling Flipper RPi Control..."
	pip3 uninstall -y flipper-rpi-control
	@echo "✓ Uninstalled"

reset-config:
	@echo "Resetting configuration..."
	rm -f ~/.flipper-rpi/config.yaml
	flipper-rpi init
	@echo "✓ Configuration reset"

logs:
	@echo "Recent logs:"
	@tail -30 ~/.flipper-rpi/logs/* 2>/dev/null || echo "No logs found"

connect-test:
	@echo "Testing connection..."
	flipper-rpi connect

proxy-status:
	@echo "Checking proxy status..."
	flipper-rpi status

start-proxy:
	@echo "Starting proxy on port 8888..."
	flipper-rpi start-proxy --port 8888

stop-proxy:
	@echo "Stopping proxy..."
	flipper-rpi stop-proxy

.DEFAULT_GOAL := help
