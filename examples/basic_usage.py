#!/usr/bin/env python3
"""
Basic usage example of the Knowledge Assistant API.

This script demonstrates how to use the Knowledge Assistant
programmatically in your own Python applications.
"""

import sys
import os

# Add parent directory to path to import knowledge_assistant
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge_assistant.knowledge_assistant import KnowledgeAssistant


def main():
    """Demonstrate basic usage of Knowledge Assistant."""
    
    print("="*80)
    print("Knowledge Assistant - Basic Usage Example")
    print("="*80)
    
    # Initialize the assistant
    print("\n1. Initializing Knowledge Assistant...")
    assistant = KnowledgeAssistant(config_path="config.yaml")
    assistant.initialize()
    
    # Option A: Index new documents
    print("\n2. Indexing documents...")
    try:
        stats = assistant.load_and_index_documents()
        print(f"   ✓ Indexed {stats['documents_loaded']} documents")
        print(f"   ✓ Created {stats['chunks_created']} chunks")
    except Exception as e:
        print(f"   Note: {e}")
        print("   Loading existing index instead...")
        assistant.load_existing_index()
    
    # Query the knowledge base
    print("\n3. Querying knowledge base...")
    
    questions = [
        "What is LangChain?",
        "How do vector embeddings work?",
        "What is RAG?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n   Query {i}: {question}")
        result = assistant.query(question)
        
        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Confidence: {result['confidence']:.1%}")
        print(f"   Sources: {result['num_sources']} documents")
        
        # Show first source
        if result['sources']:
            source = result['sources'][0]
            print(f"   Top source: {source['file_name']} (relevance: {source['relevance_score']:.1%})")
    
    print("\n" + "="*80)
    print("Example complete!")
    print("="*80)


if __name__ == '__main__':
    main()
