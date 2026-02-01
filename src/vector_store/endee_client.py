"""Endee vector database client wrapper."""

from typing import List, Dict, Optional, Any
from endee import Endee, Precision

from ..utils import settings, log


class EndeeClient:
    """Wrapper for Endee vector database client."""
    
    def __init__(
        self,
        auth_token: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize Endee client.
        
        Args:
            auth_token: Authentication token (optional)
            base_url: Base URL for Endee server
        """
        self.auth_token = auth_token or settings.endee_auth_token
        self.base_url = base_url or settings.endee_base_url
        
        log.info(f"Connecting to Endee at {self.base_url}")
        
        try:
            if self.auth_token:
                self.client = Endee(self.auth_token)
            else:
                self.client = Endee()
            
            # Set custom base URL if provided
            if self.base_url != "http://localhost:8080/api/v1":
                self.client.set_base_url(self.base_url)
            
            log.info("Endee client initialized successfully")
            
        except Exception as e:
            log.error(f"Failed to initialize Endee client: {e}")
            raise
    
    def create_index(
        self,
        name: str,
        dimension: int,
        space_type: str = "cosine",
        precision: str = "INT8D",
        m: int = 16,
        ef_con: int = 200
    ) -> bool:
        """
        Create a new vector index.
        
        Args:
            name: Index name
            dimension: Vector dimension
            space_type: Distance metric ('cosine', 'l2', 'ip')
            precision: Quantization precision
            m: HNSW M parameter
            ef_con: HNSW ef_construction parameter
            
        Returns:
            True if successful
        """
        try:
            # Map precision string to Precision enum
            precision_map = {
                "INT8D": Precision.INT8D,
                "INT16D": Precision.INT16D,
                "FLOAT16": Precision.FLOAT16,
                "FLOAT32": Precision.FLOAT32
            }
            
            precision_enum = precision_map.get(precision, Precision.INT8D)
            
            self.client.create_index(
                name=name,
                dimension=dimension,
                space_type=space_type,
                precision=precision_enum,
                M=m,
                ef_con=ef_con
            )
            
            log.info(f"Created index '{name}' with dimension {dimension}")
            return True
            
        except Exception as e:
            log.error(f"Error creating index: {e}")
            return False
    
    def get_index(self, name: str):
        """
        Get reference to an existing index.
        
        Args:
            name: Index name
            
        Returns:
            Index object
        """
        try:
            index = self.client.get_index(name=name)
            log.debug(f"Retrieved index '{name}'")
            return index
        except Exception as e:
            log.error(f"Error getting index '{name}': {e}")
            return None
    
    def list_indexes(self) -> List[str]:
        """
        List all indexes.
        
        Returns:
            List of index names
        """
        try:
            response = self.client.list_indexes()
            # API returns a dict with 'indexes' key
            if isinstance(response, dict) and 'indexes' in response:
                index_names = [idx['name'] for idx in response['indexes']]
                log.debug(f"Found {len(index_names)} indexes: {index_names}")
                return index_names
            log.warning(f"Unexpected response: {type(response)}")
            return []
        except Exception as e:
            log.error(f"Error listing indexes: {e}")
            return []
    
    def delete_index(self, name: str) -> bool:
        """
        Delete an index.
        
        Args:
            name: Index name
            
        Returns:
            True if successful
        """
        try:
            self.client.delete_index(name=name)
            log.info(f"Deleted index '{name}'")
            return True
        except Exception as e:
            log.error(f"Error deleting index '{name}': {e}")
            return False
    
    def index_exists(self, name: str) -> bool:
        """
        Check if an index exists.
        
        Args:
            name: Index name
            
        Returns:
            True if index exists
        """
        indexes = self.list_indexes()
        return name in indexes
