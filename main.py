#!/usr/bin/env python3
"""Main entry point for the Knowledge Assistant application."""

import sys
import argparse
from pathlib import Path
from knowledge_assistant.knowledge_assistant import KnowledgeAssistant


def index_documents(args):
    """Index documents from the specified directory."""
    assistant = KnowledgeAssistant(config_path=args.config)
    
    try:
        stats = assistant.load_and_index_documents()
        
        if stats['status'] == 'success':
            print(f"\n✓ Successfully indexed {stats['documents_loaded']} documents")
            print(f"✓ Created {stats['chunks_created']} text chunks")
            print(f"✓ Vector store saved to disk")
        else:
            print(f"\n✗ Error: {stats['message']}")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n✗ Error during indexing: {e}")
        sys.exit(1)


def query_interactive(args):
    """Start interactive query mode."""
    assistant = KnowledgeAssistant(config_path=args.config)
    
    try:
        # Load existing index
        assistant.load_existing_index()
        
        print("\n" + "="*80)
        print("Knowledge Assistant - Interactive Query Mode")
        print("="*80)
        print("\nType your questions below. Type 'exit' or 'quit' to stop.\n")
        
        while True:
            try:
                question = input("\n❓ Question: ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye!")
                    break
                
                print("\n🔍 Searching knowledge base...")
                result = assistant.query(question)
                assistant.display_result(result)
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\n✗ Error processing query: {e}")
    
    except FileNotFoundError:
        print("\n✗ Error: Vector store not found. Please run 'index' command first.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error loading index: {e}")
        sys.exit(1)


def query_single(args):
    """Process a single query."""
    assistant = KnowledgeAssistant(config_path=args.config)
    
    try:
        # Load existing index
        assistant.load_existing_index()
        
        print(f"\n❓ Question: {args.question}")
        print("\n🔍 Searching knowledge base...")
        
        result = assistant.query(args.question)
        assistant.display_result(result)
    
    except FileNotFoundError:
        print("\n✗ Error: Vector store not found. Please run 'index' command first.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


def add_documents_cmd(args):
    """Add new documents to the existing index."""
    assistant = KnowledgeAssistant(config_path=args.config)
    
    try:
        assistant.load_existing_index()
        
        stats = assistant.add_documents(args.directory)
        
        if stats['status'] == 'success':
            print(f"\n✓ Successfully added {stats['documents_added']} new documents")
            print(f"✓ Created {stats['chunks_added']} new chunks")
        else:
            print(f"\n✗ Error: {stats['message']}")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Knowledge Assistant - LangChain-based personal knowledge base manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Index documents from default directory
  python main.py index

  # Start interactive query mode
  python main.py query

  # Ask a single question
  python main.py ask "What is machine learning?"

  # Add new documents to existing index
  python main.py add /path/to/new/documents
        """
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Index command
    index_parser = subparsers.add_parser(
        'index',
        help='Index documents from the configured directory'
    )
    index_parser.set_defaults(func=index_documents)
    
    # Query command (interactive)
    query_parser = subparsers.add_parser(
        'query',
        help='Start interactive query mode'
    )
    query_parser.set_defaults(func=query_interactive)
    
    # Ask command (single query)
    ask_parser = subparsers.add_parser(
        'ask',
        help='Ask a single question'
    )
    ask_parser.add_argument('question', help='Question to ask')
    ask_parser.set_defaults(func=query_single)
    
    # Add command
    add_parser = subparsers.add_parser(
        'add',
        help='Add new documents to existing index'
    )
    add_parser.add_argument('directory', help='Directory containing new documents')
    add_parser.set_defaults(func=add_documents_cmd)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
