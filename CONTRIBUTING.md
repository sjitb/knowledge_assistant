# Contributing to Knowledge Assistant

Thank you for your interest in contributing to Knowledge Assistant! This document provides guidelines and instructions for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.8+
- Poetry (recommended) or pip
- Git
- OpenAI API key (for testing)

### Setting Up Your Development Environment

#### With Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/sjitb/knowledge_assistant.git
cd knowledge_assistant

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies including dev tools
poetry install

# Activate the Poetry shell
poetry shell
```

#### With pip

```bash
# Clone the repository
git clone https://github.com/sjitb/knowledge_assistant.git
cd knowledge_assistant

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov black flake8 mypy isort
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

Edit files in the `knowledge_assistant/` directory or other relevant locations.

### 3. Format Your Code

**With Poetry/Makefile:**
```bash
make format
```

**Manually:**
```bash
poetry run black knowledge_assistant/ main.py
poetry run isort knowledge_assistant/ main.py
```

### 4. Run Linters

**With Poetry/Makefile:**
```bash
make lint
```

**Manually:**
```bash
poetry run flake8 knowledge_assistant/
poetry run mypy knowledge_assistant/
```

### 5. Run Tests

**With Poetry/Makefile:**
```bash
make test
```

**Manually:**
```bash
poetry run python test_app.py
```

### 6. Test Your Changes

Test the application manually:

```bash
# Index test documents
poetry run python main.py index

# Try a query
poetry run python main.py ask "What is LangChain?"
```

### 7. Commit Your Changes

```bash
git add .
git commit -m "feat: Add new feature description"
# or
git commit -m "fix: Fix bug description"
```

Use conventional commit messages:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `style:` - Code style changes (formatting, etc.)
- `chore:` - Maintenance tasks

### 8. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python Style Guidelines

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 100 characters (configured in pyproject.toml)
- Use descriptive variable and function names
- Add docstrings to all public functions and classes

### Example

```python
from typing import List, Dict, Any
from langchain_core.documents import Document


def process_documents(documents: List[Document], chunk_size: int = 1000) -> List[Document]:
    """Process documents by splitting them into chunks.
    
    Args:
        documents: List of Document objects to process
        chunk_size: Size of each chunk in characters
        
    Returns:
        List of processed Document chunks
    """
    # Implementation here
    pass
```

## Testing

### Running the Test Suite

```bash
# Run all tests
make test

# Run with coverage
make coverage
```

### Adding New Tests

Create test files in the root directory or a `tests/` directory:

```python
# test_new_feature.py
def test_new_feature():
    """Test description."""
    # Test implementation
    assert True
```

## Documentation

### Updating Documentation

When adding new features, update:

1. **README.md** - Add to features list if user-facing
2. **SETUP.md** or **INSTALL_POETRY.md** - If installation changes
3. **Docstrings** - In all new functions and classes
4. **config.yaml** - If adding new configuration options

### Documentation Style

- Use clear, concise language
- Include code examples for new features
- Add screenshots for UI changes (if applicable)
- Update table of contents if adding major sections

## Adding New Features

### Checklist for New Features

- [ ] Code follows project style guidelines
- [ ] Code is properly formatted (black, isort)
- [ ] Linters pass (flake8, mypy)
- [ ] Tests are added and passing
- [ ] Documentation is updated
- [ ] Changes are committed with descriptive messages
- [ ] Pull request includes description of changes

### Module Organization

```
knowledge_assistant/
├── __init__.py              # Package initialization
├── config_loader.py         # Configuration management
├── document_loader.py       # Document loading
├── text_processor.py        # Text chunking
├── vector_store.py          # Vector database operations
├── query_engine.py          # Query processing
└── knowledge_assistant.py   # Main application class
```

## Adding New Dependencies

### With Poetry

```bash
# Add production dependency
poetry add package-name

# Add development dependency
poetry add --group dev package-name

# Update lock file
poetry lock
```

### With pip

Add to `requirements.txt` and run:
```bash
pip install -r requirements.txt
```

## Common Tasks

### Adding Support for New Document Types

1. Update `document_loader.py`:
   - Add file extension to supported list
   - Add loader for the new type
2. Update `config.yaml`:
   - Add extension to `supported_extensions`
3. Update documentation
4. Test with sample files

### Adding New Embedding Providers

1. Update `vector_store.py`:
   - Add new embeddings initialization
2. Update `config.yaml`:
   - Add new provider configuration
3. Update documentation
4. Test with the new provider

### Adding New LLM Providers

1. Update `query_engine.py`:
   - Add new LLM initialization
2. Update `config.yaml`:
   - Add new provider configuration
3. Update documentation
4. Test query functionality

## Troubleshooting Development Issues

### Import Errors

```bash
# Reinstall dependencies
poetry install
# or
pip install -r requirements.txt
```

### Format/Lint Errors

```bash
# Auto-fix formatting
make format

# Check what linter found
make lint
```

### Test Failures

```bash
# Run tests in verbose mode
poetry run pytest -vv

# Run specific test
poetry run pytest test_app.py::test_imports -vv
```

## Release Process

For maintainers:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md (if exists)
3. Run full test suite
4. Build package: `poetry build`
5. Create git tag: `git tag v1.0.0`
6. Push tag: `git push origin v1.0.0`
7. Publish to PyPI: `poetry publish`

## Getting Help

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check README.md, SETUP.md, INSTALL_POETRY.md

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the problem, not the person
- Welcome newcomers and help them learn

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Thank you for contributing to Knowledge Assistant! Your efforts help make this project better for everyone.
