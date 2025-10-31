# Installing Knowledge Assistant with Poetry

This guide covers installation using Poetry, a modern Python dependency management tool.

## Why Poetry?

Poetry provides:
- **Deterministic builds**: Lock file ensures reproducible installations
- **Dependency resolution**: Automatically resolves conflicts
- **Virtual environment management**: Built-in venv handling
- **Easy packaging**: Simple build and publish commands
- **Better security**: Dependency verification and vulnerability scanning

## Prerequisites

- Python 3.8 or higher
- curl (for Poetry installation)

## Installation Steps

### 1. Install Poetry

**On Linux/macOS/WSL:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**On Windows (PowerShell):**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

**Add Poetry to PATH:**

Add this to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc
```

**Verify installation:**
```bash
poetry --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/sjitb/knowledge_assistant.git
cd knowledge_assistant
```

### 3. Install Dependencies with Poetry

**Install all dependencies (including dev dependencies):**
```bash
poetry install
```

**Install production dependencies only:**
```bash
poetry install --no-dev
```

This will:
- Create a virtual environment automatically
- Install all dependencies from `pyproject.toml`
- Generate a `poetry.lock` file for reproducible builds

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 5. Activate the Poetry Environment

**Option A: Use Poetry run (recommended):**
```bash
# Run any command in the Poetry environment
poetry run python main.py index
poetry run python main.py query
```

**Option B: Enter Poetry shell:**
```bash
# Activate the virtual environment
poetry shell

# Now you can run commands directly
python main.py index
python main.py query

# Exit the shell
exit
```

## Using the Makefile

We provide a Makefile for common tasks:

### Setup
```bash
# Install Poetry (if not already installed)
make install-poetry

# Install project dependencies
make install
```

### Running the Application
```bash
# Index your documents
make index

# Start interactive query mode
make query

# Ask a single question
make ask q="What is LangChain?"
```

### Development
```bash
# Run tests
make test

# Run linters
make lint

# Format code
make format

# Generate coverage report
make coverage
```

### Maintenance
```bash
# Update dependencies
make update

# Clean build artifacts
make clean

# Clean vector database
make clean-db
```

## Quick Start with Poetry

### 1. Index Documents

```bash
poetry run python main.py index
```

Or with Make:
```bash
make index
```

### 2. Query Knowledge Base

**Interactive mode:**
```bash
poetry run python main.py query
```

Or:
```bash
make query
```

**Single question:**
```bash
poetry run python main.py ask "What is RAG?"
```

Or:
```bash
make ask q="What is RAG?"
```

## Managing Dependencies

### Add a New Dependency

```bash
# Add a production dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name
```

### Update Dependencies

```bash
# Update all dependencies
poetry update

# Update a specific package
poetry update package-name
```

### Remove a Dependency

```bash
poetry remove package-name
```

### Show Installed Packages

```bash
poetry show
```

### Show Dependency Tree

```bash
poetry show --tree
```

## Building and Publishing

### Build Distribution Packages

```bash
poetry build
```

This creates:
- `dist/knowledge_assistant-1.0.0.tar.gz` (source distribution)
- `dist/knowledge_assistant-1.0.0-py3-none-any.whl` (wheel)

### Publish to PyPI

```bash
# Test PyPI first
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi

# Production PyPI
poetry publish
```

## Development Workflow

### 1. Set Up Development Environment

```bash
# Install with dev dependencies
poetry install

# Activate shell
poetry shell
```

### 2. Make Code Changes

Edit files in `knowledge_assistant/` directory.

### 3. Format Code

```bash
make format
```

Or manually:
```bash
poetry run black knowledge_assistant/
poetry run isort knowledge_assistant/
```

### 4. Run Linters

```bash
make lint
```

Or manually:
```bash
poetry run flake8 knowledge_assistant/
poetry run mypy knowledge_assistant/
```

### 5. Run Tests

```bash
make test
```

Or manually:
```bash
poetry run pytest
```

### 6. Check Coverage

```bash
make coverage
```

Then open `htmlcov/index.html` in your browser.

## Working with Virtual Environments

### Show Virtual Environment Info

```bash
poetry env info
```

### List Virtual Environments

```bash
poetry env list
```

### Remove Virtual Environment

```bash
poetry env remove python3
```

### Use Specific Python Version

```bash
poetry env use python3.11
poetry install
```

## Troubleshooting

### Poetry Not Found After Installation

Add Poetry to your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Virtual Environment Issues

Remove and recreate the environment:
```bash
poetry env remove python3
poetry install
```

### Dependency Conflicts

Clear the cache and reinstall:
```bash
poetry cache clear pypi --all
poetry install
```

### Lock File Out of Date

Update the lock file:
```bash
poetry lock --no-update
```

Or update dependencies:
```bash
poetry update
```

## Poetry Configuration

### Common Configuration Options

```bash
# Use in-project virtual environments
poetry config virtualenvs.in-project true

# Disable virtual environment creation
poetry config virtualenvs.create false

# Set custom cache directory
poetry config cache-dir /custom/cache/path
```

### Show Current Configuration

```bash
poetry config --list
```

## Comparison: pip vs Poetry

| Task | pip | Poetry |
|------|-----|--------|
| Install dependencies | `pip install -r requirements.txt` | `poetry install` |
| Add dependency | Edit requirements.txt + `pip install` | `poetry add package` |
| Update dependencies | `pip install --upgrade` | `poetry update` |
| Lock dependencies | `pip freeze > requirements.txt` | `poetry lock` |
| Run command | `python main.py` | `poetry run python main.py` |
| Activate venv | `source venv/bin/activate` | `poetry shell` |

## Additional Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [pyproject.toml Specification](https://python-poetry.org/docs/pyproject/)
- [Poetry Commands Reference](https://python-poetry.org/docs/cli/)
- [Dependency Management](https://python-poetry.org/docs/dependency-specification/)

## Support

For issues with Poetry setup:
- Poetry Issues: https://github.com/python-poetry/poetry/issues
- Project Issues: https://github.com/sjitb/knowledge_assistant/issues
