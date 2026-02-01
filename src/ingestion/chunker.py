"""Text chunking strategies for document processing."""

from typing import List, Dict
import tiktoken

from ..utils import settings, log


class TextChunker:
    """Chunk text into smaller segments for embedding."""
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
        encoding_name: str = "cl100k_base"
    ):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Maximum tokens per chunk
            chunk_overlap: Number of overlapping tokens between chunks
            encoding_name: Tokenizer encoding name
        """
        self.chunk_size = chunk_size or settings.max_chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        try:
            self.encoding = tiktoken.get_encoding(encoding_name)
        except Exception as e:
            log.warning(f"Could not load tiktoken encoding: {e}. Using character-based chunking.")
            self.encoding = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.encoding:
            return len(self.encoding.encode(text))
        else:
            # Rough approximation: 1 token ≈ 4 characters
            return len(text) // 4
    
    def chunk_by_tokens(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Chunk text by token count with overlap.
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of chunk dictionaries
        """
        if not text:
            return []
        
        metadata = metadata or {}
        chunks = []
        
        if self.encoding:
            tokens = self.encoding.encode(text)
            
            start = 0
            chunk_id = 0
            
            while start < len(tokens):
                end = start + self.chunk_size
                chunk_tokens = tokens[start:end]
                chunk_text = self.encoding.decode(chunk_tokens)
                
                chunks.append({
                    "text": chunk_text,
                    "chunk_id": chunk_id,
                    "start_token": start,
                    "end_token": end,
                    "token_count": len(chunk_tokens),
                    **metadata
                })
                
                start += self.chunk_size - self.chunk_overlap
                chunk_id += 1
        else:
            # Fallback: character-based chunking
            char_chunk_size = self.chunk_size * 4
            char_overlap = self.chunk_overlap * 4
            
            start = 0
            chunk_id = 0
            
            while start < len(text):
                end = start + char_chunk_size
                chunk_text = text[start:end]
                
                chunks.append({
                    "text": chunk_text,
                    "chunk_id": chunk_id,
                    "start_char": start,
                    "end_char": end,
                    "char_count": len(chunk_text),
                    **metadata
                })
                
                start += char_chunk_size - char_overlap
                chunk_id += 1
        
        log.info(f"Created {len(chunks)} chunks from text ({self.count_tokens(text)} tokens)")
        return chunks
    
    def chunk_by_sentences(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Chunk text by sentences while respecting token limits.
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of chunk dictionaries
        """
        if not text:
            return []
        
        metadata = metadata or {}
        
        # Simple sentence splitting (can be improved with NLTK)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        chunk_id = 0
        
        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)
            
            if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "chunk_id": chunk_id,
                    "token_count": current_tokens,
                    **metadata
                })
                
                # Start new chunk with overlap
                overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
                current_chunk = overlap_sentences + [sentence]
                current_tokens = sum(self.count_tokens(s) for s in current_chunk)
                chunk_id += 1
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
        
        # Add final chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "chunk_id": chunk_id,
                "token_count": current_tokens,
                **metadata
            })
        
        log.info(f"Created {len(chunks)} sentence-based chunks")
        return chunks
    
    def chunk_document(self, document: Dict, strategy: str = "tokens") -> List[Dict]:
        """
        Chunk a document using specified strategy.
        
        Args:
            document: Document dictionary with 'text' and metadata
            strategy: Chunking strategy ('tokens' or 'sentences')
            
        Returns:
            List of chunk dictionaries
        """
        text = document.get("text", "")
        metadata = {k: v for k, v in document.items() if k != "text"}
        
        if strategy == "tokens":
            return self.chunk_by_tokens(text, metadata)
        elif strategy == "sentences":
            return self.chunk_by_sentences(text, metadata)
        else:
            log.warning(f"Unknown chunking strategy: {strategy}. Using 'tokens'.")
            return self.chunk_by_tokens(text, metadata)


import re
