"""Embedding model wrapper for generating vector representations."""

from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

from ..utils import settings, log


class EmbeddingModel:
    """Wrapper for sentence transformer embedding model."""
    
    def __init__(self, model_name: str = None):
        """
        Initialize embedding model.
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name or settings.embedding_model
        self.dimension = settings.embedding_dimension
        
        log.info(f"Loading embedding model: {self.model_name}")
        try:
            self.model = SentenceTransformer(self.model_name)
            log.info(f"Embedding model loaded successfully. Dimension: {self.dimension}")
        except Exception as e:
            log.error(f"Failed to load embedding model: {e}")
            raise
    
    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 32,
        show_progress: bool = False
    ) -> np.ndarray:
        """
        Generate embeddings for text(s).
        
        Args:
            texts: Single text or list of texts
            batch_size: Batch size for encoding
            show_progress: Whether to show progress bar
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True
            )
            
            log.debug(f"Generated embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            log.error(f"Error generating embeddings: {e}")
            raise
    
    def encode_single(self, text: str) -> List[float]:
        """
        Encode a single text and return as list.
        
        Args:
            text: Text to encode
            
        Returns:
            Embedding as list of floats
        """
        embedding = self.encode(text)
        return embedding[0].tolist()
    
    def encode_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Encode multiple texts in batches.
        
        Args:
            texts: List of texts
            batch_size: Batch size
            
        Returns:
            List of embeddings
        """
        embeddings = self.encode(texts, batch_size=batch_size, show_progress=True)
        return embeddings.tolist()
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.dimension
