.PHONY: help format lint type-check security test clean install update-hooks all pre-commit test-fast

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

format: ## Format code with Ruff
	ruff format .
	ruff check --fix .

lint: ## Lint code with Ruff (no fixes)
	ruff check .

type-check: ## Run type checking with mypy
	mypy applyr/

security: ## Run security scan with bandit
	bandit -r applyr/ -f json -o bandit-report.json || true
	@echo "Security report saved to bandit-report.json"

test: ## Run tests with coverage
	pytest --cov=applyr --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without coverage
	pytest

clean: ## Clean cache and temporary files
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -r {} + 2>/dev/null || true
	rm -rf .coverage htmlcov .pytest_cache .mypy_cache .ruff_cache bandit-report.json

install: ## Install dependencies and pre-commit hooks
	poetry install
	pre-commit install

update-hooks: ## Update pre-commit hooks to latest versions
	pre-commit autoupdate

all: format lint type-check security test ## Run all checks

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files
