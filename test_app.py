#!/usr/bin/env python3
"""
Test script for the Knowledge Assistant application.
This script tests the core functionality without requiring full dependencies.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from knowledge_assistant.config_loader import ConfigLoader
        print("✓ ConfigLoader imported")
    except ImportError as e:
        print(f"✗ ConfigLoader import failed: {e}")
        return False
    
    try:
        from knowledge_assistant.document_loader import DocumentLoader
        print("✓ DocumentLoader imported")
    except ImportError as e:
        print(f"✗ DocumentLoader import failed: {e}")
        return False
    
    try:
        from knowledge_assistant.text_processor import TextProcessor
        print("✓ TextProcessor imported")
    except ImportError as e:
        print(f"✗ TextProcessor import failed: {e}")
        return False
    
    try:
        from knowledge_assistant.vector_store import VectorStoreManager
        print("✓ VectorStoreManager imported")
    except ImportError as e:
        print(f"✗ VectorStoreManager import failed: {e}")
        return False
    
    try:
        from knowledge_assistant.query_engine import QueryEngine
        print("✓ QueryEngine imported")
    except ImportError as e:
        print(f"✗ QueryEngine import failed: {e}")
        return False
    
    try:
        from knowledge_assistant.knowledge_assistant import KnowledgeAssistant
        print("✓ KnowledgeAssistant imported")
    except ImportError as e:
        print(f"✗ KnowledgeAssistant import failed: {e}")
        return False
    
    return True


def test_config_loader():
    """Test the configuration loader."""
    print("\nTesting ConfigLoader...")
    
    try:
        from knowledge_assistant.config_loader import ConfigLoader
        
        config = ConfigLoader('config.yaml')
        print(f"✓ Config loaded successfully")
        
        doc_config = config.get_document_loader_config()
        print(f"✓ Document loader config: {doc_config.get('input_directory')}")
        
        text_config = config.get_text_splitter_config()
        print(f"✓ Text splitter config: chunk_size={text_config.get('chunk_size')}")
        
        return True
    except Exception as e:
        print(f"✗ ConfigLoader test failed: {e}")
        return False


def test_document_structure():
    """Test if document directory exists and has files."""
    print("\nTesting document structure...")
    
    import os
    from pathlib import Path
    
    doc_dir = Path("./documents")
    if not doc_dir.exists():
        print(f"✗ Documents directory not found: {doc_dir}")
        return False
    
    print(f"✓ Documents directory exists: {doc_dir}")
    
    files = list(doc_dir.rglob("*.txt"))
    print(f"✓ Found {len(files)} .txt files")
    
    for file in files[:3]:  # Show first 3 files
        print(f"  - {file.name}")
    
    return len(files) > 0


def test_text_processing():
    """Test text processing functionality."""
    print("\nTesting text processing...")
    
    try:
        from knowledge_assistant.text_processor import TextProcessor
        from langchain_core.documents import Document
        
        processor = TextProcessor(chunk_size=100, chunk_overlap=20)
        print("✓ TextProcessor initialized")
        
        # Create test document
        test_doc = Document(
            page_content="This is a test document. " * 20,
            metadata={'source': 'test.txt'}
        )
        
        chunks = processor.split_documents([test_doc])
        print(f"✓ Text split into {len(chunks)} chunks")
        
        stats = processor.get_chunk_stats(chunks)
        print(f"✓ Chunk stats: {stats['total_chunks']} chunks, avg size: {stats['avg_chunk_size']:.0f}")
        
        return True
    except Exception as e:
        print(f"✗ Text processing test failed: {e}")
        return False


def test_main_cli():
    """Test if main CLI can be invoked."""
    print("\nTesting main CLI...")
    
    try:
        import main
        print("✓ Main CLI module can be imported")
        return True
    except ImportError as e:
        print(f"✗ Main CLI import failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("="*80)
    print("Knowledge Assistant Test Suite")
    print("="*80)
    
    results = []
    
    results.append(("Import Tests", test_imports()))
    results.append(("Config Loader", test_config_loader()))
    results.append(("Document Structure", test_document_structure()))
    results.append(("Text Processing", test_text_processing()))
    results.append(("Main CLI", test_main_cli()))
    
    print("\n" + "="*80)
    print("Test Summary")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*80)
    
    return passed == total


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
