"""Vector indexer for storing embeddings in Endee."""

from typing import List, Dict, Any
from tqdm import tqdm

from .endee_client import EndeeClient
from ..utils import settings, log


class VectorIndexer:
    """Index vectors in Endee database."""
    
    def __init__(self, client: EndeeClient = None):
        """
        Initialize vector indexer.
        
        Args:
            client: Endee client instance
        """
        self.client = client or EndeeClient()
        self.index_name = settings.index_name
        self.index = None
    
    def setup_index(
        self,
        dimension: int = None,
        force_recreate: bool = False
    ) -> bool:
        """
        Setup vector index (create if doesn't exist).
        
        Args:
            dimension: Vector dimension
            force_recreate: Whether to delete and recreate existing index
            
        Returns:
            True if successful
        """
        dimension = dimension or settings.embedding_dimension
        
        # Check if index exists
        if self.client.index_exists(self.index_name):
            if force_recreate:
                log.warning(f"Deleting existing index '{self.index_name}'")
                self.client.delete_index(self.index_name)
                # Will create new index below
            else:
                log.info(f"Index '{self.index_name}' already exists, using it")
                self.index = self.client.get_index(self.index_name)
                log.info(f"Index '{self.index_name}' setup complete")
                return True
        
        # Create new index
        success = self.client.create_index(
            name=self.index_name,
            dimension=dimension,
            space_type=settings.space_type,
            precision=settings.precision
        )
        
        if success:
            self.index = self.client.get_index(self.index_name)
            log.info(f"Index '{self.index_name}' setup complete")
        
        return success
    
    def upsert_vectors(
        self,
        vectors: List[List[float]],
        ids: List[str],
        metadata: List[Dict[str, Any]] = None,
        filters: List[Dict[str, Any]] = None,
        batch_size: int = 100
    ) -> int:
        """
        Upsert vectors to index in batches.
        
        Args:
            vectors: List of vector embeddings
            ids: List of unique IDs
            metadata: List of metadata dictionaries
            filters: List of filter dictionaries
            batch_size: Batch size for upserting
            
        Returns:
            Number of vectors upserted
        """
        if not self.index:
            log.error("Index not initialized. Call setup_index() first.")
            return 0
        
        if len(vectors) != len(ids):
            log.error("Number of vectors and IDs must match")
            return 0
        
        metadata = metadata or [{} for _ in range(len(vectors))]
        filters = filters or [{} for _ in range(len(vectors))]
        
        total_upserted = 0
        
        # Process in batches
        for i in tqdm(range(0, len(vectors), batch_size), desc="Upserting vectors"):
            batch_end = min(i + batch_size, len(vectors))
            
            batch_data = [
                {
                    "id": ids[j],
                    "vector": vectors[j],
                    "meta": metadata[j],
                    "filter": filters[j]
                }
                for j in range(i, batch_end)
            ]
            
            try:
                self.index.upsert(batch_data)
                total_upserted += len(batch_data)
            except Exception as e:
                log.error(f"Error upserting batch {i}-{batch_end}: {e}")
        
        log.info(f"Upserted {total_upserted} vectors to index '{self.index_name}'")
        return total_upserted
    
    def upsert_chunks(self, chunks: List[Dict], embeddings: List[List[float]]) -> int:
        """
        Upsert document chunks with embeddings.
        
        Args:
            chunks: List of chunk dictionaries
            embeddings: List of embeddings
            
        Returns:
            Number of chunks upserted
        """
        if len(chunks) != len(embeddings):
            log.error("Number of chunks and embeddings must match")
            return 0
        
        # Prepare data
        ids = [f"{chunk.get('source', 'doc')}_{chunk.get('chunk_id', i)}" 
               for i, chunk in enumerate(chunks)]
        
        metadata = [
            {
                "text": chunk.get("text", ""),
                "source": chunk.get("source", ""),
                "filename": chunk.get("filename", ""),
                "chunk_id": chunk.get("chunk_id", i)
            }
            for i, chunk in enumerate(chunks)
        ]
        
        filters = [
            {
                "format": chunk.get("format", ""),
                "filename": chunk.get("filename", "")
            }
            for chunk in chunks
        ]
        
        return self.upsert_vectors(embeddings, ids, metadata, filters)
