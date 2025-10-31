"""Configuration loader for the Knowledge Assistant."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """Loads and manages configuration settings."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the config loader.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file.
        
        Returns:
            Dictionary containing configuration settings
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key.
        
        Args:
            key: Configuration key (supports nested keys with dot notation)
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_document_loader_config(self) -> Dict[str, Any]:
        """Get document loader configuration."""
        return self.config.get('document_loader', {})
    
    def get_text_splitter_config(self) -> Dict[str, Any]:
        """Get text splitter configuration."""
        return self.config.get('text_splitter', {})
    
    def get_embeddings_config(self) -> Dict[str, Any]:
        """Get embeddings configuration."""
        return self.config.get('embeddings', {})
    
    def get_vector_store_config(self) -> Dict[str, Any]:
        """Get vector store configuration."""
        return self.config.get('vector_store', {})
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        return self.config.get('llm', {})
    
    def get_query_config(self) -> Dict[str, Any]:
        """Get query configuration."""
        return self.config.get('query', {})
