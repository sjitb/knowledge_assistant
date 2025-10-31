"""Main Knowledge Assistant application class."""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

from .config_loader import ConfigLoader
from .document_loader import DocumentLoader
from .text_processor import TextProcessor
from .vector_store import VectorStoreManager
from .query_engine import QueryEngine


class KnowledgeAssistant:
    """Main class for the Knowledge Assistant application."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the Knowledge Assistant.
        
        Args:
            config_path: Path to the configuration file
        """
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        self.config = ConfigLoader(config_path)
        
        # Initialize components
        self.document_loader = None
        self.text_processor = None
        self.vector_store_manager = None
        self.query_engine = None
        
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize all components of the Knowledge Assistant."""
        print("Initializing Knowledge Assistant...")
        
        # Initialize document loader
        doc_config = self.config.get_document_loader_config()
        self.document_loader = DocumentLoader(
            input_directory=doc_config.get('input_directory', './documents'),
            supported_extensions=doc_config.get('supported_extensions')
        )
        
        # Initialize text processor
        text_config = self.config.get_text_splitter_config()
        self.text_processor = TextProcessor(
            chunk_size=text_config.get('chunk_size', 1000),
            chunk_overlap=text_config.get('chunk_overlap', 200)
        )
        
        # Initialize vector store
        vec_config = self.config.get_vector_store_config()
        emb_config = self.config.get_embeddings_config()
        
        use_openai = emb_config.get('provider') == 'openai'
        
        self.vector_store_manager = VectorStoreManager(
            embeddings_model=emb_config.get('model', 'sentence-transformers/all-MiniLM-L6-v2'),
            persist_directory=vec_config.get('persist_directory', './chroma_db'),
            collection_name=vec_config.get('collection_name', 'knowledge_base'),
            use_openai_embeddings=use_openai
        )
        
        self._initialized = True
        print("Knowledge Assistant initialized successfully!")
    
    def load_and_index_documents(self) -> Dict[str, Any]:
        """Load documents from directory and create vector index.
        
        Returns:
            Dictionary containing statistics about the indexing process
        """
        if not self._initialized:
            self.initialize()
        
        print("\n--- Loading Documents ---")
        
        # Load documents
        documents = self.document_loader.load_documents()
        doc_count = len(documents)
        print(f"Loaded {doc_count} documents")
        
        if doc_count == 0:
            return {
                'status': 'error',
                'message': 'No documents found to index',
                'documents_loaded': 0,
                'chunks_created': 0
            }
        
        print("\n--- Splitting Documents ---")
        
        # Split documents into chunks
        chunks = self.text_processor.split_documents(documents)
        chunk_stats = self.text_processor.get_chunk_stats(chunks)
        
        print(f"Created {chunk_stats['total_chunks']} chunks")
        print(f"Average chunk size: {chunk_stats['avg_chunk_size']:.0f} characters")
        
        print("\n--- Creating Vector Store ---")
        
        # Create vector store
        self.vector_store_manager.create_vector_store(chunks)
        
        # Initialize query engine
        self._initialize_query_engine()
        
        return {
            'status': 'success',
            'documents_loaded': doc_count,
            'chunks_created': chunk_stats['total_chunks'],
            'chunk_stats': chunk_stats
        }
    
    def load_existing_index(self) -> None:
        """Load an existing vector store index from disk."""
        if not self._initialized:
            self.initialize()
        
        print("Loading existing vector store...")
        self.vector_store_manager.load_vector_store()
        
        # Initialize query engine
        self._initialize_query_engine()
        
        print("Existing index loaded successfully!")
    
    def _initialize_query_engine(self) -> None:
        """Initialize the query engine with current configuration."""
        llm_config = self.config.get_llm_config()
        query_config = self.config.get_query_config()
        
        self.query_engine = QueryEngine(
            vector_store_manager=self.vector_store_manager,
            model=llm_config.get('model', 'gpt-3.5-turbo'),
            temperature=llm_config.get('temperature', 0.7),
            max_tokens=llm_config.get('max_tokens', 500),
            top_k=query_config.get('top_k', 4)
        )
    
    def query(self, question: str, score_threshold: Optional[float] = None) -> Dict[str, Any]:
        """Query the knowledge base with a natural language question.
        
        Args:
            question: Natural language question
            score_threshold: Minimum relevance score for results
            
        Returns:
            Dictionary containing answer, sources, and metadata
        """
        if self.query_engine is None:
            raise ValueError("Query engine not initialized. Load or create an index first.")
        
        if score_threshold is None:
            score_threshold = self.config.get('query.score_threshold')
        
        return self.query_engine.query(question, score_threshold)
    
    def display_result(self, result: Dict[str, Any]) -> None:
        """Display query result in a formatted way.
        
        Args:
            result: Query result dictionary
        """
        print("\n" + "="*80)
        print("ANSWER")
        print("="*80)
        print(result['answer'])
        
        print("\n" + "="*80)
        print(f"SOURCES (Confidence: {result.get('confidence', 0):.1%})")
        print("="*80)
        
        for i, source in enumerate(result.get('sources', []), 1):
            print(f"\n[{i}] {source['file_name']}")
            print(f"    Relevance: {source['relevance_score']:.1%}")
            print(f"    Chunk ID: {source['chunk_id']}")
            print(f"    Preview: {source['content_preview'][:150]}...")
        
        print("\n" + "="*80)
        print(f"Total sources used: {result.get('num_sources', 0)}")
        print("="*80 + "\n")
    
    def add_documents(self, new_doc_directory: str) -> Dict[str, Any]:
        """Add new documents to the existing index.
        
        Args:
            new_doc_directory: Path to directory containing new documents
            
        Returns:
            Dictionary containing statistics about the added documents
        """
        if self.vector_store_manager is None or self.vector_store_manager.vector_store is None:
            raise ValueError("Vector store not initialized. Load or create an index first.")
        
        # Load new documents
        temp_loader = DocumentLoader(
            input_directory=new_doc_directory,
            supported_extensions=self.document_loader.supported_extensions
        )
        
        documents = temp_loader.load_documents()
        print(f"Loaded {len(documents)} new documents")
        
        if len(documents) == 0:
            return {
                'status': 'error',
                'message': 'No new documents found',
                'documents_added': 0
            }
        
        # Split documents
        chunks = self.text_processor.split_documents(documents)
        print(f"Created {len(chunks)} new chunks")
        
        # Add to vector store
        self.vector_store_manager.add_documents(chunks)
        
        return {
            'status': 'success',
            'documents_added': len(documents),
            'chunks_added': len(chunks)
        }
