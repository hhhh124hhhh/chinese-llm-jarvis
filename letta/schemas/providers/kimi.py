from typing import List, Optional

from letta.schemas.embedding_config import EmbeddingConfig
from letta.schemas.llm_config import LLMConfig
from letta.schemas.providers.base import Provider
from letta.settings import model_settings


class KimiProvider(Provider):
    """Kimi (Moonshot AI) provider implementation"""
    
    def list_llm_models(self) -> List[LLMConfig]:
        """List available Kimi models with their configurations"""
        # Kimi models with their context window sizes
        kimi_models = {
            "moonshot-v1-8k": 8192,
            "moonshot-v1-32k": 32768,
            "moonshot-v1-128k": 131072,
            "kimi-k2-0905-preview": 262144,  # 256K context
            "kimi-k2-0711-preview": 131072,  # 128K context
            "kimi-k2-turbo-preview": 262144,  # 256K context
        }
        
        configs = []
        for model_name, context_window in kimi_models.items():
            configs.append(
                LLMConfig(
                    model=model_name,
                    model_endpoint_type="openai",
                    model_endpoint=model_settings.kimi_base_url,
                    context_window=context_window,
                    handle=self.get_handle(model_name),
                    provider_name=self.name,
                    provider_category=self.provider_category,
                    model_wrapper=None,
                    put_inner_thoughts_in_kwargs=True,
                    temperature=0.7,
                    max_tokens=None,
                    enable_reasoner=True,
                    reasoning_effort=None,
                    max_reasoning_tokens=0,
                    frequency_penalty=None,
                    compatibility_type=None,
                    verbosity=None,
                    tier=None,
                )
            )
        
        return configs

    async def list_llm_models_async(self) -> List[LLMConfig]:
        """Async version of listing Kimi models"""
        return self.list_llm_models()

    def list_embedding_models(self) -> List[EmbeddingConfig]:
        """List available Kimi embedding models"""
        # Kimi currently doesn't have dedicated embedding models
        # Using default embedding models
        return []

    def get_handle(self, model_name: str, is_embedding: bool = False, base_name: Optional[str] = None) -> str:
        """Generate handle for the model"""
        model = model_name.split("/")[-1] if "/" in model_name else model_name
        return f"{self.name}/{model}"