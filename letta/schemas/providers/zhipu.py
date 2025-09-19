from typing import List, Optional

from letta.schemas.embedding_config import EmbeddingConfig
from letta.schemas.llm_config import LLMConfig
from letta.schemas.providers.base import Provider
from letta.settings import model_settings


class ZhipuProvider(Provider):
    """Zhipu AI (智谱AI) provider implementation"""
    
    def list_llm_models(self) -> List[LLMConfig]:
        """List available Zhipu models with their configurations"""
        # Zhipu models with their context window sizes
        zhipu_models = {
            "glm-4-plus": 128000,
            "glm-4-0520": 128000,
            "glm-4": 128000,
            "glm-4-air": 128000,
            "glm-4-airx": 128000,
            "glm-4-long": 1000000,  # 1M context
            "glm-4-flash": 128000,
            "glm-4-flashx": 128000,
            "glm-5": 128000,
        }
        
        configs = []
        for model_name, context_window in zhipu_models.items():
            configs.append(
                LLMConfig(
                    model=model_name,
                    model_endpoint_type="openai",
                    model_endpoint=model_settings.zhipu_base_url,
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
        """Async version of listing Zhipu models"""
        return self.list_llm_models()

    def list_embedding_models(self) -> List[EmbeddingConfig]:
        """List available Zhipu embedding models"""
        # Zhipu embedding models
        embedding_models = {
            "embedding-2": 2048,
            "embedding-3": 2048,
        }
        
        configs = []
        for model_name, dim in embedding_models.items():
            configs.append(
                EmbeddingConfig(
                    embedding_model=model_name,
                    embedding_endpoint_type="openai",
                    embedding_endpoint=model_settings.zhipu_base_url,
                    embedding_dim=dim,
                    embedding_chunk_size=300,
                    handle=self.get_handle(model_name, is_embedding=True),
                    batch_size=1024,
                    azure_endpoint=None,
                    azure_version=None,
                    azure_deployment=None,
                )
            )
        
        return configs

    def get_handle(self, model_name: str, is_embedding: bool = False, base_name: Optional[str] = None) -> str:
        """Generate handle for the model"""
        model = model_name.split("/")[-1] if "/" in model_name else model_name
        return f"{self.name}/{model}"