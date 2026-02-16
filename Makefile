.PHONY: help up down build lint test test-backend test-frontend security-scan format clean setup

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## First-time setup: copy env, install hooks, build containers
	@if not exist .env copy .env.example .env
	cd backend && pip install pre-commit && pre-commit install
	$(MAKE) build
	$(MAKE) up

up: ## Start all services via docker-compose
	docker compose -f infra/docker/docker-compose.yml --env-file .env up -d

down: ## Stop all services
	docker compose -f infra/docker/docker-compose.yml down

build: ## Build all Docker images
	docker compose -f infra/docker/docker-compose.yml --env-file .env build

lint: ## Run all linters
	cd backend && ruff check . && ruff format --check .
	cd frontend && npx eslint .

format: ## Auto-format code
	cd backend && ruff format . && ruff check --fix .

test: test-backend test-frontend ## Run all tests

test-backend: ## Run backend tests with coverage
	cd backend && python -m pytest --cov=app --cov-report=term-missing --cov-report=xml

test-frontend: ## Run frontend tests with coverage
	cd frontend && npx jest --coverage

security-scan: ## Run security scans
	cd backend && bandit -r app -f json && pip-audit
	cd frontend && npm audit

clean: ## Remove build artifacts and caches
	del /s /q __pycache__ 2>nul
	del /s /q .pytest_cache 2>nul
	del /s /q htmlcov 2>nul
	del /q coverage.xml 2>nul
	if exist frontend\dist rmdir /s /q frontend\dist

logs: ## Tail all service logs
	docker compose -f infra/docker/docker-compose.yml logs -f

logs-backend: ## Tail backend logs
	docker compose -f infra/docker/docker-compose.yml logs -f backend

restart-backend: ## Restart backend service
	docker compose -f infra/docker/docker-compose.yml restart backend
