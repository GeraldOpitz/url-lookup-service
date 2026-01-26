DOCKER := docker
ifeq ($(OS),Windows_NT)
	DOCKER := docker.exe
endif

PROJECT_NAME = url-lookup-service
DB_NAME = url_lookup

VENV = .venv
PYTHON := $(shell command -v python3 || command -v python)

PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

ifeq ($(OS),Windows_NT)
	PIP := $(VENV)/Scripts/pip.exe
	PY := $(VENV)/Scripts/python.exe
endif

.PHONY: setup venv install test docker-up docker-down logs clean db

setup: venv install
	@echo "Local environment ready."

venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
	else \
		echo "Virtual environment already exists."; \
	fi

install:
	@echo "Installing dependencies..."
	@$(PIP) install .

test:
	@echo "Running tests..."
	@$(PY) -m pytest -v --cov=app


docker-up:
	@echo "Starting Docker containers..."
	@$(DOCKER) compose -p $(PROJECT_NAME) up --build -d

docker-down:
	@echo "Stopping Docker containers..."
	@$(DOCKER) compose -p $(PROJECT_NAME) down
logs:
	@$(DOCKER) compose -p $(PROJECT_NAME) logs -f api

db:
	@$(DOCKER) compose exec db psql -U postgres -d $(DB_NAME)

clean:
	@echo "Cleaning project..."
	@$(DOCKER) compose -p $(PROJECT_NAME) down --rmi all -v --remove-orphans || true
	@rm -rf $(VENV)
	@find . -type d -name "__pycache__" -exec rm -rf {} + || true
	@rm -rf .pytest_cache
	@echo "Clean completed."
