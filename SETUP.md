# Knowledge Assistant - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key (for answer generation)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/sjitb/knowledge_assistant.git
cd knowledge_assistant
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

Install all required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

If you encounter network issues, install packages individually:

```bash
# Core LangChain packages
pip install langchain langchain-community langchain-openai

# Vector store and embeddings
pip install chromadb sentence-transformers

# Document loaders
pip install pypdf python-docx unstructured

# Utilities
pip install python-dotenv pyyaml openai tiktoken
```

### 4. Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-api-key-here
```

To get an OpenAI API key:
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it in your `.env` file

### 5. Verify Installation

Run the test script to verify everything is set up correctly:

```bash
python3 test_app.py
```

Expected output:
```
================================================================================
Knowledge Assistant Test Suite
================================================================================
Testing imports...
✓ ConfigLoader imported
✓ DocumentLoader imported
✓ TextProcessor imported
✓ VectorStoreManager imported
✓ QueryEngine imported
✓ KnowledgeAssistant imported
...
Total: 5/5 tests passed
```

## Quick Start

### 1. Add Your Documents

Place your documents in the `documents/` directory. Supported formats:
- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.docx` - Microsoft Word documents
- `.md` - Markdown files

Sample documents are already included for testing.

### 2. Index Your Documents

Create the vector index from your documents:

```bash
python main.py index
```

This will:
- Load all documents from the `documents/` directory
- Split them into chunks (default: 1000 chars with 200 char overlap)
- Generate embeddings using Sentence Transformers
- Store embeddings in ChromaDB

Expected output:
```
Initializing Knowledge Assistant...
Knowledge Assistant initialized successfully!

--- Loading Documents ---
Loaded 3 documents

--- Splitting Documents ---
Created 12 chunks
Average chunk size: 850 characters

--- Creating Vector Store ---
Vector store created with 12 documents

✓ Successfully indexed 3 documents
✓ Created 12 text chunks
✓ Vector store saved to disk
```

### 3. Query Your Knowledge Base

#### Interactive Mode

Start an interactive session:

```bash
python main.py query
```

Then ask questions:
```
❓ Question: What is LangChain?
🔍 Searching knowledge base...

================================================================================
ANSWER
================================================================================
LangChain is a framework for developing applications powered by language 
models. It enables applications that are context-aware and can reason about 
how to answer based on provided context...
```

#### Single Query Mode

Ask a single question:

```bash
python main.py ask "What is RAG?"
```

### 4. Add More Documents (Optional)

Add new documents to your existing index:

```bash
python main.py add /path/to/new/documents
```

## Configuration

Edit `config.yaml` to customize settings:

### Document Loading

```yaml
document_loader:
  input_directory: "./documents"
  supported_extensions: [.txt, .pdf, .docx, .md]
```

### Text Chunking

```yaml
text_splitter:
  chunk_size: 1000        # Characters per chunk
  chunk_overlap: 200      # Overlapping characters
```

### Embeddings

For local embeddings (default, no API key needed):
```yaml
embeddings:
  model: "sentence-transformers/all-MiniLM-L6-v2"
```

For OpenAI embeddings (requires API key):
```yaml
embeddings:
  provider: "openai"
  model: "text-embedding-ada-002"
```

### LLM Settings

```yaml
llm:
  provider: "openai"
  model: "gpt-3.5-turbo"    # or "gpt-4"
  temperature: 0.7          # 0.0-1.0 (higher = more creative)
  max_tokens: 500           # Maximum response length
```

### Query Settings

```yaml
query:
  top_k: 4                  # Number of chunks to retrieve
  score_threshold: 0.5      # Minimum relevance score (0.0-1.0)
```

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### OpenAI API Errors

If you get authentication errors:
1. Check that `.env` file exists and contains your API key
2. Verify the API key is valid at https://platform.openai.com/api-keys
3. Ensure you have credits/billing set up in your OpenAI account

### No Documents Found

If indexing fails with "No documents found":
1. Check that documents are in the correct directory
2. Verify file extensions are supported
3. Check file permissions

### Memory Issues

If you encounter out-of-memory errors:
1. Reduce `chunk_size` in config.yaml
2. Reduce `top_k` in config.yaml
3. Use a smaller embedding model
4. Process fewer documents at once

### ChromaDB Errors

If you get ChromaDB errors:
```bash
# Delete the existing database and recreate
rm -rf chroma_db/
python main.py index
```

## Advanced Usage

### Using Different LLM Models

Edit `config.yaml`:
```yaml
llm:
  model: "gpt-4"  # More capable but more expensive
  # or
  model: "gpt-3.5-turbo-16k"  # Larger context window
```

### Custom Chunk Sizes

For code or technical documents:
```yaml
text_splitter:
  chunk_size: 1500
  chunk_overlap: 300
```

For shorter content (tweets, comments):
```yaml
text_splitter:
  chunk_size: 500
  chunk_overlap: 100
```

### Using a Custom Config File

```bash
python main.py --config my_custom_config.yaml index
python main.py --config my_custom_config.yaml query
```

## Testing

Run the test suite:
```bash
python3 test_app.py
```

Check syntax:
```bash
python3 -m py_compile knowledge_assistant/*.py main.py
```

## Deployment

### Production Considerations

1. **API Key Security**: Never commit `.env` file to version control
2. **Rate Limiting**: Implement rate limiting for OpenAI API calls
3. **Caching**: Cache frequent queries to reduce API costs
4. **Monitoring**: Log API usage and costs
5. **Backup**: Regularly backup your `chroma_db/` directory

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py", "query"]
```

Build and run:
```bash
docker build -t knowledge-assistant .
docker run -it --env-file .env -v $(pwd)/documents:/app/documents knowledge-assistant
```

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/sjitb/knowledge_assistant/issues
- Documentation: See README.md

## Next Steps

1. Add your own documents to the `documents/` directory
2. Run `python main.py index` to create your knowledge base
3. Start querying with `python main.py query`
4. Customize `config.yaml` for your specific needs
5. Explore the codebase in `knowledge_assistant/` directory
