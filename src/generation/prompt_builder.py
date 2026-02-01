"""Prompt builder for RAG system."""

from typing import List, Dict, Any


class PromptBuilder:
    """Build prompts for RAG question answering."""
    
    def __init__(self):
        """Initialize prompt builder."""
        self.system_prompt = self._get_default_system_prompt()
    
    def _get_default_system_prompt(self) -> str:
        """Get default system prompt for RAG."""
        return """You are a helpful technical documentation assistant. Your role is to answer questions based ONLY on the provided context from technical documentation.

Guidelines:
1. Answer questions using ONLY the information in the provided context
2. If the answer is not in the context, say "I don't have enough information to answer this question based on the available documentation."
3. Be precise and technical when appropriate
4. Always cite the source document when providing information
5. Do not make assumptions or add information not present in the context
6. If multiple sources provide relevant information, synthesize them clearly

Remember: Accuracy is more important than completeness. It's better to say you don't know than to provide incorrect information."""
    
    def build_rag_prompt(
        self,
        query: str,
        context: str,
        include_instructions: bool = True
    ) -> str:
        """
        Build RAG prompt with query and context.
        
        Args:
            query: User question
            context: Retrieved context
            include_instructions: Whether to include answering instructions
            
        Returns:
            Formatted prompt
        """
        prompt_parts = []
        
        if include_instructions:
            prompt_parts.append("Please answer the following question using the provided context.\n")
        
        prompt_parts.append(f"CONTEXT:\n{context}\n")
        prompt_parts.append(f"QUESTION:\n{query}\n")
        prompt_parts.append("ANSWER:")
        
        return "\n".join(prompt_parts)
    
    def build_prompt_with_results(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> str:
        """
        Build prompt from search results.
        
        Args:
            query: User question
            results: Search results from vector store
            
        Returns:
            Formatted prompt
        """
        if not results:
            context = "No relevant documentation found."
        else:
            context_parts = []
            for i, result in enumerate(results, 1):
                meta = result.get('meta', {})
                text = meta.get('text', '')
                source = meta.get('source', 'Unknown')
                similarity = result.get('similarity', 0)
                
                context_parts.append(
                    f"[Source {i}] {source} (Relevance: {similarity:.2%})\n{text}"
                )
            
            context = "\n\n---\n\n".join(context_parts)
        
        return self.build_rag_prompt(query, context)
    
    def set_system_prompt(self, prompt: str):
        """Set custom system prompt."""
        self.system_prompt = prompt
    
    def get_system_prompt(self) -> str:
        """Get current system prompt."""
        return self.system_prompt
