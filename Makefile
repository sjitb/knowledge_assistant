.PHONY: install install-poetry test lint format clean index query help

help:
	@echo "Knowledge Assistant - Makefile Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install-poetry  Install Poetry package manager"
	@echo "  make install         Install project dependencies with Poetry"
	@echo ""
	@echo "Development:"
	@echo "  make test           Run tests with pytest"
	@echo "  make lint           Run linters (flake8, mypy)"
	@echo "  make format         Format code with black and isort"
	@echo "  make clean          Clean build artifacts and cache"
	@echo ""
	@echo "Application:"
	@echo "  make index          Index documents in the documents/ directory"
	@echo "  make query          Start interactive query mode"
	@echo ""

install-poetry:
	@echo "Installing Poetry..."
	curl -sSL https://install.python-poetry.org | python3 -
	@echo "Poetry installed! Add to PATH: export PATH=\"\$$HOME/.local/bin:\$$PATH\""

install:
	@echo "Installing dependencies with Poetry..."
	poetry install

install-prod:
	@echo "Installing production dependencies only..."
	poetry install --no-dev

update:
	@echo "Updating dependencies..."
	poetry update

test:
	@echo "Running tests..."
	poetry run pytest

test-verbose:
	@echo "Running tests with verbose output..."
	poetry run pytest -vv

coverage:
	@echo "Running tests with coverage report..."
	poetry run pytest --cov=knowledge_assistant --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	@echo "Running flake8..."
	poetry run flake8 knowledge_assistant/ main.py
	@echo "Running mypy..."
	poetry run mypy knowledge_assistant/

format:
	@echo "Formatting code with black..."
	poetry run black knowledge_assistant/ main.py test_app.py
	@echo "Sorting imports with isort..."
	poetry run isort knowledge_assistant/ main.py test_app.py

format-check:
	@echo "Checking code format..."
	poetry run black --check knowledge_assistant/ main.py test_app.py
	poetry run isort --check knowledge_assistant/ main.py test_app.py

clean:
	@echo "Cleaning build artifacts and cache..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

clean-db:
	@echo "Cleaning vector database..."
	rm -rf chroma_db/
	@echo "Vector database removed!"

index:
	@echo "Indexing documents..."
	poetry run python main.py index

query:
	@echo "Starting interactive query mode..."
	poetry run python main.py query

ask:
	@if [ -z "$(q)" ]; then \
		echo "Usage: make ask q=\"Your question here\""; \
	else \
		poetry run python main.py ask "$(q)"; \
	fi

shell:
	@echo "Starting Poetry shell..."
	poetry shell

build:
	@echo "Building package..."
	poetry build

publish:
	@echo "Publishing to PyPI..."
	poetry publish --build

run-test-script:
	@echo "Running test script..."
	poetry run python test_app.py
