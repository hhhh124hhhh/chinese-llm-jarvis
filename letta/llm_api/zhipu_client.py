import os
from typing import List, Optional

from letta.llm_api.llm_client_base import LLMClientBase
from letta.llm_api.openai_client import OpenAIClient
from letta.schemas.embedding_config import EmbeddingConfig
from letta.schemas.llm_config import LLMConfig
from letta.settings import model_settings


class ZhipuClient(OpenAIClient):
    """Zhipu AI (智谱AI) client - inherits from OpenAI client since the API is compatible"""
    
    def _prepare_client_kwargs(self, llm_config: LLMConfig) -> dict:
        """Prepare client configuration for Zhipu API"""
        api_key = model_settings.zhipu_api_key or os.environ.get("ZHIPU_API_KEY")
        # Use default Zhipu base URL if not specified in llm_config
        base_url = llm_config.model_endpoint or model_settings.zhipu_base_url
        
        # Zhipu requires a valid API key
        if not api_key:
            raise ValueError("Zhipu API key is required. Please set ZHIPU_API_KEY in your environment or in settings.")
            
        kwargs = {"api_key": api_key, "base_url": base_url}
        return kwargs

    def _prepare_client_kwargs_embedding(self, embedding_config: EmbeddingConfig) -> dict:
        """Prepare client configuration for Zhipu embeddings"""
        api_key = model_settings.zhipu_api_key or os.environ.get("ZHIPU_API_KEY")
        base_url = embedding_config.embedding_endpoint or model_settings.zhipu_base_url
        
        if not api_key:
            raise ValueError("Zhipu API key is required for embeddings.")
            
        kwargs = {"api_key": api_key, "base_url": base_url}
        return kwargs

    async def _prepare_client_kwargs_async(self, llm_config: LLMConfig) -> dict:
        """Prepare async client configuration for Zhipu API"""
        api_key = model_settings.zhipu_api_key or os.environ.get("ZHIPU_API_KEY")
        base_url = llm_config.model_endpoint or model_settings.zhipu_base_url
        
        if not api_key:
            raise ValueError("Zhipu API key is required.")
            
        kwargs = {"api_key": api_key, "base_url": base_url}
        return kwargs

    def requires_auto_tool_choice(self, llm_config: LLMConfig) -> bool:
        """Zhipu may require auto tool choice for certain models"""
        # GLM-4 and newer models may require auto tool choice
        if llm_config.model and "glm" in llm_config.model.lower():
            # GLM-4 models with tool calling capabilities
            if any(version in llm_config.model.lower() for version in ["glm-4", "glm-5"]):
                return True
        return super().requires_auto_tool_choice(llm_config)

    def supports_structured_output(self, llm_config: LLMConfig) -> bool:
        """Zhipu supports structured output for newer models"""
        # GLM-4 and newer models support structured output
        if llm_config.model and "glm" in llm_config.model.lower():
            if any(version in llm_config.model.lower() for version in ["glm-4", "glm-5"]):
                return True
        return super().supports_structured_output(llm_config)