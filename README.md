# Knowledge Assistant

A LangChain-based agentic application for managing and querying a personal knowledge base. This tool allows you to index documents, generate embeddings, and perform natural language queries with source citations and confidence scores.

## Features

- 📚 **Document Loading**: Load documents from a specified directory (supports .txt, .pdf, .docx, .md)
- ✂️ **Smart Chunking**: Split documents into chunks with configurable size and overlap
- 🧠 **Vector Embeddings**: Generate embeddings using Sentence Transformers or OpenAI
- 🔍 **Semantic Search**: Retrieve relevant document chunks using vector similarity
- 💬 **Natural Language Queries**: Ask questions in natural language
- 📖 **Source Citations**: Get answers with source attribution
- 📊 **Confidence Scores**: View relevance metrics for each source
- 🔄 **Incremental Updates**: Add new documents to existing index

## Technical Stack

- **Python 3.8+**
- **LangChain**: Primary orchestration framework
- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: Local embeddings generation
- **OpenAI**: LLM for answer generation (requires API key)

## Installation

### Option 1: Poetry (Recommended)

[Poetry](https://python-poetry.org/) is the recommended package manager for this project.

1. **Install Poetry**:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Clone the repository**:
```bash
git clone https://github.com/sjitb/knowledge_assistant.git
cd knowledge_assistant
```

3. **Install dependencies**:
```bash
poetry install
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

See [INSTALL_POETRY.md](INSTALL_POETRY.md) for detailed Poetry installation and usage instructions.

### Option 2: pip

1. **Clone the repository**:
```bash
git clone https://github.com/sjitb/knowledge_assistant.git
cd knowledge_assistant
```

2. **Create virtual environment** (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

See [SETUP.md](SETUP.md) for detailed pip installation instructions.

### Configuration (Optional)

Edit `config.yaml` to customize:
- Document directory
- Chunk size and overlap
- Embedding model
- LLM settings
- Retrieval parameters

## Quick Start

### 1. Index Documents

Place your documents in the `documents/` directory (or configure a custom path in `config.yaml`), then run:

**With Poetry:**
```bash
poetry run python main.py index
# Or use the Makefile
make index
```

**With pip:**
```bash
python main.py index
```

This will:
- Load all supported documents
- Split them into chunks
- Generate embeddings
- Store in ChromaDB vector database

### 2. Query Your Knowledge Base

**Interactive mode:**

With Poetry:
```bash
poetry run python main.py query
# Or
make query
```

With pip:
```bash
python main.py query
```

**Single question:**

With Poetry:
```bash
poetry run python main.py ask "What is LangChain?"
# Or
make ask q="What is LangChain?"
```

With pip:
```bash
python main.py ask "What is LangChain?"
```

### 3. Add New Documents

**With Poetry:**
```bash
poetry run python main.py add /path/to/new/documents
```

**With pip:**
```bash
python main.py add /path/to/new/documents
```

## Usage Examples

### Indexing Documents

**With Poetry:**
```bash
# Index documents from default directory
poetry run python main.py index

# Use custom config
poetry run python main.py --config custom_config.yaml index

# Or use Makefile
make index
```

**With pip:**
```bash
# Index documents from default directory
python main.py index

# Use custom config
python main.py --config custom_config.yaml index
```

### Querying

**Interactive Mode**:
```bash
$ python main.py query

Knowledge Assistant - Interactive Query Mode
================================================================================

Type your questions below. Type 'exit' or 'quit' to stop.

❓ Question: What is RAG?

🔍 Searching knowledge base...

================================================================================
ANSWER
================================================================================
RAG (Retrieval Augmented Generation) is a technique that enhances language 
models by retrieving relevant information from external knowledge sources before 
generating responses...

================================================================================
SOURCES (Confidence: 85.3%)
================================================================================

[1] sample_rag.txt
    Relevance: 89.2%
    Chunk ID: 0
    Preview: Retrieval Augmented Generation (RAG)...
```

**Single Query**:
```bash
python main.py ask "How do vector embeddings work?"
```

### Adding Documents
```bash
# Add documents from a new directory
python main.py add ./new_documents

# Add documents with custom config
python main.py --config my_config.yaml add ./new_documents
```

## Configuration

The `config.yaml` file contains all configuration options:

```yaml
# Document processing
document_loader:
  input_directory: "./documents"
  supported_extensions: [.txt, .pdf, .docx, .md]

# Text splitting
text_splitter:
  chunk_size: 1000
  chunk_overlap: 200

# Embeddings
embeddings:
  model: "sentence-transformers/all-MiniLM-L6-v2"

# Vector store
vector_store:
  type: "chroma"
  persist_directory: "./chroma_db"

# LLM settings
llm:
  provider: "openai"
  model: "gpt-3.5-turbo"
  temperature: 0.7

# Query settings
query:
  top_k: 4
  score_threshold: 0.5
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Knowledge Assistant                      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   Document   │      │     Text     │     │    Vector    │
│    Loader    │─────▶│   Processor  │────▶│    Store     │
└──────────────┘      └──────────────┘     └──────────────┘
        │                     │                     │
        │                     │                     ▼
        │                     │              ┌──────────────┐
        │                     └─────────────▶│    Query     │
        │                                    │    Engine    │
        └───────────────────────────────────▶└──────────────┘
                                                    │
                                                    ▼
                                            ┌──────────────┐
                                            │  LLM (GPT)   │
                                            └──────────────┘
```

## Module Overview

- **`config_loader.py`**: Loads and manages YAML configuration
- **`document_loader.py`**: Loads documents from directories
- **`text_processor.py`**: Splits documents into chunks
- **`vector_store.py`**: Manages embeddings and vector database
- **`query_engine.py`**: Processes queries and generates answers
- **`knowledge_assistant.py`**: Main application class
- **`main.py`**: CLI entry point

## Requirements

See `requirements.txt` for full dependency list. Key dependencies:
- langchain >= 0.1.0
- chromadb >= 0.4.22
- sentence-transformers >= 2.2.2
- openai >= 1.7.2
- pypdf >= 3.17.4
- python-docx >= 1.1.0

## API Key Setup

This application uses OpenAI's API for answer generation. You need an API key:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Add it to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

## Troubleshooting

**Issue**: `Vector store not found`
- **Solution**: Run `python main.py index` first to create the index

**Issue**: `OpenAI API key not found`
- **Solution**: Ensure your `.env` file contains a valid `OPENAI_API_KEY`

**Issue**: `No documents found`
- **Solution**: Add documents to the `documents/` directory or configure a different path

**Issue**: `Out of memory`
- **Solution**: Reduce `chunk_size` and `top_k` in `config.yaml`, or use smaller embedding models

## Advanced Usage

### Using OpenAI Embeddings

Edit `config.yaml`:
```yaml
embeddings:
  provider: "openai"
  model: "text-embedding-ada-002"
```

### Customizing Chunk Size

For technical documents with code:
```yaml
text_splitter:
  chunk_size: 1500
  chunk_overlap: 300
```

For short-form content:
```yaml
text_splitter:
  chunk_size: 500
  chunk_overlap: 100
```

### Adjusting Retrieval Parameters

For more sources:
```yaml
query:
  top_k: 6
  score_threshold: 0.4
```

For higher precision:
```yaml
query:
  top_k: 3
  score_threshold: 0.7
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Uses [ChromaDB](https://www.trychroma.com/) for vector storage
- Powered by [Sentence Transformers](https://www.sbert.net/)
