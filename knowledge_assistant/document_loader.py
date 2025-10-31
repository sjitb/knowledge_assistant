"""Document loader module for loading documents from a directory."""

import os
from pathlib import Path
from typing import List, Optional
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    DirectoryLoader,
)
from langchain_core.documents import Document


class DocumentLoader:
    """Loads documents from a specified directory."""
    
    def __init__(self, input_directory: str, supported_extensions: Optional[List[str]] = None):
        """Initialize the document loader.
        
        Args:
            input_directory: Path to the directory containing documents
            supported_extensions: List of supported file extensions (default: ['.txt', '.pdf', '.docx', '.md'])
        """
        self.input_directory = Path(input_directory)
        self.supported_extensions = supported_extensions or ['.txt', '.pdf', '.docx', '.md']
        
        if not self.input_directory.exists():
            raise FileNotFoundError(f"Input directory not found: {self.input_directory}")
    
    def load_documents(self) -> List[Document]:
        """Load all supported documents from the input directory.
        
        Returns:
            List of Document objects
        """
        all_documents = []
        
        for extension in self.supported_extensions:
            documents = self._load_documents_by_extension(extension)
            all_documents.extend(documents)
        
        return all_documents
    
    def _load_documents_by_extension(self, extension: str) -> List[Document]:
        """Load documents of a specific extension.
        
        Args:
            extension: File extension to load (e.g., '.txt', '.pdf')
            
        Returns:
            List of Document objects
        """
        documents = []
        
        # Find all files with the given extension
        for file_path in self.input_directory.rglob(f"*{extension}"):
            try:
                doc = self._load_single_document(file_path)
                if doc:
                    documents.extend(doc)
            except Exception as e:
                print(f"Warning: Failed to load {file_path}: {e}")
        
        return documents
    
    def _load_single_document(self, file_path: Path) -> Optional[List[Document]]:
        """Load a single document based on its extension.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of Document objects or None if loading fails
        """
        extension = file_path.suffix.lower()
        
        try:
            if extension == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif extension == '.docx':
                loader = Docx2txtLoader(str(file_path))
            elif extension in ['.txt', '.md']:
                loader = TextLoader(str(file_path))
            else:
                print(f"Unsupported file type: {extension}")
                return None
            
            documents = loader.load()
            
            # Add source metadata
            for doc in documents:
                doc.metadata['source'] = str(file_path)
                doc.metadata['file_name'] = file_path.name
            
            return documents
        
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def get_document_count(self) -> int:
        """Get the count of supported documents in the directory.
        
        Returns:
            Number of supported documents
        """
        count = 0
        for extension in self.supported_extensions:
            count += len(list(self.input_directory.rglob(f"*{extension}")))
        return count
