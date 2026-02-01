"""LLM client wrapper for answer generation (OpenAI and Groq)."""

from typing import Optional, List, Dict
import openai
from groq import Groq

from ..utils import settings, log


class LLMClient:
    """Wrapper for LLM API (OpenAI or Groq)."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, provider: Optional[str] = None):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key for LLM provider
            model: Model name
            provider: Provider name ('openai' or 'groq')
        """
        self.provider = provider or settings.llm_provider
        self.model = model or settings.llm_model
        
        # Determine API key based on provider
        if self.provider == "groq":
            self.api_key = api_key or settings.groq_api_key
        else:
            self.api_key = api_key or settings.openai_api_key
        
        if not self.api_key:
            log.warning(f"No API key provided for {self.provider}. LLM generation will not work.")
            self.client = None
        else:
            if self.provider == "groq":
                self.client = Groq(api_key=self.api_key)
                log.info(f"Groq client initialized with model: {self.model}")
            else:
                openai.api_key = self.api_key
                self.client = openai
                log.info(f"OpenAI client initialized with model: {self.model}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> str:
        """
        Generate text using LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        if not self.client:
            return f"Error: LLM client not initialized. Please provide a {self.provider.upper()} API key."
        
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            if self.provider == "groq":
                # Groq API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            else:
                # OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            
            answer = response.choices[0].message.content
            log.debug(f"Generated {len(answer)} characters using {self.provider}")
            
            return answer
            
        except Exception as e:
            log.error(f"Error generating response with {self.provider}: {e}")
            return f"Error generating response: {str(e)}"
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 500
    ) -> str:
        """
        Chat with LLM using message history.
        
        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        if not self.client:
            return f"Error: LLM client not initialized. Please provide a {self.provider.upper()} API key."
        
        try:
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            
            return response.choices[0].message.content
            
        except Exception as e:
            log.error(f"Error in chat with {self.provider}: {e}")
            return f"Error: {str(e)}"
