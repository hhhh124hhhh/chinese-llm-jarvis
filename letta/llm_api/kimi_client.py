import os
from typing import List, Optional

from letta.llm_api.llm_client_base import LLMClientBase
from letta.llm_api.openai_client import OpenAIClient
from letta.schemas.embedding_config import EmbeddingConfig
from letta.schemas.llm_config import LLMConfig
from letta.settings import model_settings


class KimiClient(OpenAIClient):
    """Kimi API client (Moonshot AI) - inherits from OpenAI client since the API is compatible"""
    
    def _prepare_client_kwargs(self, llm_config: LLMConfig) -> dict:
        """Prepare client configuration for Kimi API"""
        api_key = model_settings.kimi_api_key or os.environ.get("KIMI_API_KEY")
        # Use default Kimi base URL if not specified in llm_config
        base_url = llm_config.model_endpoint or model_settings.kimi_base_url
        
        # Kimi requires a valid API key
        if not api_key:
            raise ValueError("Kimi API key is required. Please set KIMI_API_KEY in your environment or in settings.")
            
        kwargs = {"api_key": api_key, "base_url": base_url}
        return kwargs

    def _prepare_client_kwargs_embedding(self, embedding_config: EmbeddingConfig) -> dict:
        """Prepare client configuration for Kimi embeddings (if supported)"""
        api_key = model_settings.kimi_api_key or os.environ.get("KIMI_API_KEY")
        base_url = embedding_config.embedding_endpoint or model_settings.kimi_base_url
        
        if not api_key:
            raise ValueError("Kimi API key is required for embeddings.")
            
        kwargs = {"api_key": api_key, "base_url": base_url}
        return kwargs

    async def _prepare_client_kwargs_async(self, llm_config: LLMConfig) -> dict:
        """Prepare async client configuration for Kimi API"""
        api_key = model_settings.kimi_api_key or os.environ.get("KIMI_API_KEY")
        base_url = llm_config.model_endpoint or model_settings.kimi_base_url
        
        if not api_key:
            raise ValueError("Kimi API key is required.")
            
        kwargs = {"api_key": api_key, "base_url": base_url}
        return kwargs

    def requires_auto_tool_choice(self, llm_config: LLMConfig) -> bool:
        """Kimi may require auto tool choice for certain models"""
        # Check if this is a Kimi K2 model which may have specific requirements
        if llm_config.model and "k2" in llm_config.model.lower():
            return True
        return super().requires_auto_tool_choice(llm_config)

    def supports_structured_output(self, llm_config: LLMConfig) -> bool:
        """Kimi supports structured output for most models"""
        # Kimi K2 models support structured output
        if llm_config.model and "k2" in llm_config.model.lower():
            return True
        return super().supports_structured_output(llm_config)