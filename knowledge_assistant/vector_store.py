"""Vector store module for managing embeddings and similarity search."""

import os
from typing import List, Optional, Tuple
from pathlib import Path
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings


class VectorStoreManager:
    """Manages vector store operations including embeddings and retrieval."""
    
    def __init__(
        self,
        embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db",
        collection_name: str = "knowledge_base",
        use_openai_embeddings: bool = False
    ):
        """Initialize the vector store manager.
        
        Args:
            embeddings_model: Name of the embeddings model to use
            persist_directory: Directory to persist the vector store
            collection_name: Name of the collection in the vector store
            use_openai_embeddings: Whether to use OpenAI embeddings instead of local
        """
        self.embeddings_model = embeddings_model
        self.persist_directory = Path(persist_directory)
        self.collection_name = collection_name
        
        # Create persist directory if it doesn't exist
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize embeddings
        if use_openai_embeddings:
            self.embeddings = OpenAIEmbeddings(model=embeddings_model)
        else:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=embeddings_model,
                model_kwargs={'device': 'cpu'}
            )
        
        self.vector_store: Optional[Chroma] = None
    
    def create_vector_store(self, documents: List[Document]) -> None:
        """Create a vector store from documents.
        
        Args:
            documents: List of Document objects to index
        """
        if not documents:
            raise ValueError("No documents provided to create vector store")
        
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=str(self.persist_directory),
            collection_name=self.collection_name
        )
        
        print(f"Vector store created with {len(documents)} documents")
    
    def load_vector_store(self) -> None:
        """Load an existing vector store from disk."""
        if not self.persist_directory.exists():
            raise FileNotFoundError(f"Vector store not found at {self.persist_directory}")
        
        self.vector_store = Chroma(
            persist_directory=str(self.persist_directory),
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )
        
        print(f"Vector store loaded from {self.persist_directory}")
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add new documents to the existing vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")
        
        self.vector_store.add_documents(documents)
        print(f"Added {len(documents)} documents to vector store")
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        score_threshold: Optional[float] = None
    ) -> List[Tuple[Document, float]]:
        """Perform similarity search with relevance scores.
        
        Args:
            query: Query string to search for
            k: Number of top results to return
            score_threshold: Minimum similarity score threshold (0-1)
            
        Returns:
            List of tuples containing (Document, relevance_score)
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")
        
        # Perform similarity search with scores
        results = self.vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=k
        )
        
        # Filter by score threshold if provided
        if score_threshold is not None:
            results = [(doc, score) for doc, score in results if score >= score_threshold]
        
        return results
    
    def as_retriever(self, k: int = 4):
        """Get the vector store as a retriever.
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            Retriever object
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Create or load a vector store first.")
        
        return self.vector_store.as_retriever(search_kwargs={"k": k})
    
    def delete_collection(self) -> None:
        """Delete the vector store collection."""
        if self.vector_store is not None:
            self.vector_store.delete_collection()
            self.vector_store = None
            print("Vector store collection deleted")
