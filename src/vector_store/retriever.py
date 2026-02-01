"""Vector retriever for querying Endee database."""

from typing import List, Dict, Any, Optional

from .endee_client import EndeeClient
from ..utils import settings, log


class VectorRetriever:
    """Retrieve similar vectors from Endee database."""
    
    def __init__(self, client: EndeeClient = None):
        """
        Initialize vector retriever.
        
        Args:
            client: Endee client instance
        """
        self.client = client or EndeeClient()
        self.index_name = settings.index_name
        self.top_k = settings.top_k
        self.index = None
        
        # Get index reference
        if self.client.index_exists(self.index_name):
            self.index = self.client.get_index(self.index_name)
        else:
            log.warning(f"Index '{self.index_name}' does not exist")
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = None,
        filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query embedding
            top_k: Number of results to return
            filters: Optional filters
            
        Returns:
            List of search results with metadata
        """
        if not self.index:
            log.error(f"Index '{self.index_name}' not available")
            return []
        
        top_k = top_k or self.top_k
        
        try:
            # Query the index
            if filters:
                results = self.index.query(
                    vector=query_vector,
                    top_k=top_k,
                    filter=filters
                )
            else:
                results = self.index.query(
                    vector=query_vector,
                    top_k=top_k
                )
            
            log.debug(f"Retrieved {len(results)} results")
            return results
            
        except Exception as e:
            log.error(f"Error searching index: {e}")
            return []
    
    def get_context(
        self,
        query_vector: List[float],
        top_k: int = None,
        min_similarity: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Get context chunks for RAG.
        
        Args:
            query_vector: Query embedding
            top_k: Number of chunks to retrieve
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of context chunks with metadata
        """
        results = self.search(query_vector, top_k)
        
        # Filter by minimum similarity
        filtered_results = [
            r for r in results 
            if r.get('similarity', 0) >= min_similarity
        ]
        
        log.info(f"Retrieved {len(filtered_results)} context chunks (min_sim={min_similarity})")
        return filtered_results
    
    def format_context(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results into context string for LLM.
        
        Args:
            results: Search results
            
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant context found."
        
        context_parts = []
        
        for i, result in enumerate(results, 1):
            meta = result.get('meta', {})
            text = meta.get('text', '')
            source = meta.get('source', 'Unknown')
            similarity = result.get('similarity', 0)
            
            context_parts.append(
                f"[Context {i}] (Similarity: {similarity:.3f})\n"
                f"Source: {source}\n"
                f"{text}\n"
            )
        
        return "\n---\n".join(context_parts)
