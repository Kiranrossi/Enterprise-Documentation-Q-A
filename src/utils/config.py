"""Configuration management for the RAG system."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Endee Configuration
    endee_host: str = Field(default="localhost", alias="ENDEE_HOST")
    endee_port: int = Field(default=8080, alias="ENDEE_PORT")
    endee_base_url: str = Field(default="http://localhost:8080/api/v1", alias="ENDEE_BASE_URL")
    endee_auth_token: Optional[str] = Field(default=None, alias="ENDEE_AUTH_TOKEN")
    
    # Embedding Model
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL"
    )
    embedding_dimension: int = Field(default=384, alias="EMBEDDING_DIMENSION")
    
    # LLM Configuration
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    groq_api_key: Optional[str] = Field(default=None, alias="GROQ_API_KEY")
    llm_provider: str = Field(default="groq", alias="LLM_PROVIDER")
    llm_model: str = Field(default="llama-3.1-70b-versatile", alias="LLM_MODEL")
    
    # Vector Index Configuration
    index_name: str = Field(default="technical_docs", alias="INDEX_NAME")
    space_type: str = Field(default="cosine", alias="SPACE_TYPE")
    precision: str = Field(default="INT8D", alias="PRECISION")
    top_k: int = Field(default=5, alias="TOP_K")
    
    # Application Settings
    app_title: str = Field(
        default="Enterprise Documentation Q&A",
        alias="APP_TITLE"
    )
    app_description: str = Field(
        default="RAG-powered technical documentation assistant",
        alias="APP_DESCRIPTION"
    )
    max_chunk_size: int = Field(default=512, alias="MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(default=50, alias="CHUNK_OVERLAP")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Paths
    project_root: Path = Path(__file__).parent.parent.parent
    data_dir: Path = project_root / "data"
    raw_data_dir: Path = data_dir / "raw"
    processed_data_dir: Path = data_dir / "processed"
    embeddings_dir: Path = data_dir / "embeddings"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories if they don't exist
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        self.embeddings_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
