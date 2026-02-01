"""RAG answer generator combining retrieval and generation."""

from typing import List, Dict, Any, Optional

from .llm_client import LLMClient
from .prompt_builder import PromptBuilder
from ..embeddings import EmbeddingModel
from ..vector_store import VectorRetriever
from ..utils import log


class RAGGenerator:
    """End-to-end RAG answer generation."""
    
    def __init__(
        self,
        embedding_model: EmbeddingModel = None,
        retriever: VectorRetriever = None,
        llm_client: LLMClient = None,
        prompt_builder: PromptBuilder = None
    ):
        """
        Initialize RAG generator.
        
        Args:
            embedding_model: Embedding model for queries
            retriever: Vector retriever
            llm_client: LLM client
            prompt_builder: Prompt builder
        """
        self.embedding_model = embedding_model or EmbeddingModel()
        self.retriever = retriever or VectorRetriever()
        self.llm_client = llm_client or LLMClient()
        self.prompt_builder = prompt_builder or PromptBuilder()
        
        log.info("RAG Generator initialized")
    
    def generate_answer(
        self,
        query: str,
        top_k: int = 5,
        min_similarity: float = 0.0,
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> Dict[str, Any]:
        """
        Generate answer for a query using RAG.
        
        Args:
            query: User question
            top_k: Number of context chunks to retrieve
            min_similarity: Minimum similarity threshold
            temperature: LLM temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        log.info(f"Generating answer for query: {query[:100]}...")
        
        # Step 1: Embed query
        try:
            query_embedding = self.embedding_model.encode_single(query)
        except Exception as e:
            log.error(f"Error embedding query: {e}")
            return {
                "query": query,
                "answer": f"Error processing query: {str(e)}",
                "sources": [],
                "error": str(e)
            }
        
        # Step 2: Retrieve context
        try:
            results = self.retriever.get_context(
                query_vector=query_embedding,
                top_k=top_k,
                min_similarity=min_similarity
            )
        except Exception as e:
            log.error(f"Error retrieving context: {e}")
            return {
                "query": query,
                "answer": f"Error retrieving context: {str(e)}",
                "sources": [],
                "error": str(e)
            }
        
        # Step 3: Build prompt
        prompt = self.prompt_builder.build_prompt_with_results(query, results)
        system_prompt = self.prompt_builder.get_system_prompt()
        
        # Step 4: Generate answer
        try:
            answer = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
        except Exception as e:
            log.error(f"Error generating answer: {e}")
            return {
                "query": query,
                "answer": f"Error generating answer: {str(e)}",
                "sources": results,
                "error": str(e)
            }
        
        # Step 5: Format response
        sources = [
            {
                "text": r.get('meta', {}).get('text', '')[:200] + "...",
                "source": r.get('meta', {}).get('source', 'Unknown'),
                "filename": r.get('meta', {}).get('filename', 'Unknown'),
                "similarity": r.get('similarity', 0)
            }
            for r in results
        ]
        
        log.info("Answer generated successfully")
        
        return {
            "query": query,
            "answer": answer,
            "sources": sources,
            "num_sources": len(sources),
            "top_similarity": sources[0]['similarity'] if sources else 0
        }
    
    def batch_generate(
        self,
        queries: List[str],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Generate answers for multiple queries.
        
        Args:
            queries: List of questions
            **kwargs: Arguments for generate_answer
            
        Returns:
            List of answer dictionaries
        """
        results = []
        for query in queries:
            result = self.generate_answer(query, **kwargs)
            results.append(result)
        
        return results
