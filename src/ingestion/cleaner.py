"""Text cleaning and preprocessing utilities."""

import re
from typing import List


class TextCleaner:
    """Clean and preprocess text for embedding."""
    
    def __init__(self):
        """Initialize text cleaner."""
        pass
    
    def clean(self, text: str) -> str:
        """
        Clean text by removing noise and normalizing.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'"\/]', '', text)
        
        # Remove multiple consecutive punctuation
        text = re.sub(r'([.,!?;:])\1+', r'\1', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    def remove_emails(self, text: str) -> str:
        """Remove email addresses from text."""
        return re.sub(r'\S+@\S+', '', text)
    
    def normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace to single spaces."""
        return ' '.join(text.split())
    
    def preprocess(self, text: str, remove_urls: bool = False, remove_emails: bool = False) -> str:
        """
        Full preprocessing pipeline.
        
        Args:
            text: Raw text
            remove_urls: Whether to remove URLs
            remove_emails: Whether to remove emails
            
        Returns:
            Preprocessed text
        """
        if remove_urls:
            text = self.remove_urls(text)
        
        if remove_emails:
            text = self.remove_emails(text)
        
        text = self.clean(text)
        text = self.normalize_whitespace(text)
        
        return text
