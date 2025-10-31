# Knowledge Assistant Examples

This directory contains example scripts demonstrating how to use Knowledge Assistant in your own applications.

## Examples

### basic_usage.py

Demonstrates the basic API usage:
- Initializing the Knowledge Assistant
- Indexing documents
- Querying the knowledge base
- Processing results

**Run:**
```bash
cd examples
python basic_usage.py
```

## Creating Your Own Scripts

### Minimal Example

```python
from knowledge_assistant.knowledge_assistant import KnowledgeAssistant

# Initialize
assistant = KnowledgeAssistant(config_path="config.yaml")
assistant.initialize()

# Load existing index or create new one
assistant.load_existing_index()
# OR: assistant.load_and_index_documents()

# Query
result = assistant.query("What is LangChain?")
print(result['answer'])
```

### Custom Configuration Example

```python
from knowledge_assistant.config_loader import ConfigLoader
from knowledge_assistant.knowledge_assistant import KnowledgeAssistant

# Load custom config
assistant = KnowledgeAssistant(config_path="my_custom_config.yaml")
assistant.initialize()
assistant.load_and_index_documents()

# Query with custom threshold
result = assistant.query("Your question", score_threshold=0.7)
```

### Processing Multiple Queries Example

```python
from knowledge_assistant.knowledge_assistant import KnowledgeAssistant

assistant = KnowledgeAssistant()
assistant.initialize()
assistant.load_existing_index()

questions = [
    "What is RAG?",
    "How do embeddings work?",
    "What is LangChain?"
]

results = []
for question in questions:
    result = assistant.query(question)
    results.append({
        'question': question,
        'answer': result['answer'],
        'confidence': result['confidence']
    })

# Process results
for r in results:
    print(f"Q: {r['question']}")
    print(f"A: {r['answer']}")
    print(f"Confidence: {r['confidence']:.1%}\n")
```

### Adding Documents Programmatically Example

```python
from knowledge_assistant.knowledge_assistant import KnowledgeAssistant

assistant = KnowledgeAssistant()
assistant.initialize()
assistant.load_existing_index()

# Add documents from a new directory
stats = assistant.add_documents("/path/to/new/documents")
print(f"Added {stats['documents_added']} documents")
```

## API Reference

### KnowledgeAssistant Class

**Initialization:**
```python
assistant = KnowledgeAssistant(config_path="config.yaml")
assistant.initialize()
```

**Methods:**

- `load_and_index_documents()`: Load documents and create vector index
- `load_existing_index()`: Load existing vector index from disk
- `query(question, score_threshold)`: Query the knowledge base
- `display_result(result)`: Display formatted result
- `add_documents(new_doc_directory)`: Add new documents to existing index

**Query Result Structure:**
```python
{
    'answer': str,           # Generated answer
    'sources': [             # List of source documents
        {
            'file_name': str,
            'source_path': str,
            'relevance_score': float,
            'chunk_id': int,
            'content_preview': str
        }
    ],
    'confidence': float,     # Overall confidence score (0-1)
    'num_sources': int      # Number of sources used
}
```

## Tips

1. **Reuse the Index**: Load an existing index instead of recreating it each time
2. **Adjust Thresholds**: Use `score_threshold` parameter to filter low-quality results
3. **Error Handling**: Wrap queries in try-except blocks for production use
4. **Environment Variables**: Ensure `.env` file is properly configured
5. **Configuration**: Customize `config.yaml` for your specific use case

## Need Help?

- Check the main [README.md](../README.md)
- Review [SETUP.md](../SETUP.md) for installation issues
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines
