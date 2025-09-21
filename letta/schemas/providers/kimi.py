from typing import List, Optional

from letta.schemas.embedding_config import EmbeddingConfig
from letta.schemas.llm_config import LLMConfig
from letta.schemas.providers.base import Provider
from letta.settings import model_settings
from letta.errors import LLMAuthenticationError, LLMError, ErrorCode, LLMPermissionDeniedError, LLMTimeoutError
import httpx
import json


class KimiProvider(Provider):
    """Kimi (Moonshot AI) provider implementation"""
    
    async def check_api_key(self):
        """Check if the API key is valid for the Kimi API"""
        if not self.api_key:
            raise ValueError("No API key provided")
        
        try:
            # Use a simple API call to verify the key
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                # Kimi API doesn't have a dedicated auth check endpoint,
                # so we'll try to get the models list as a verification
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=headers
                )
                if response.status_code == 401:
                    raise LLMAuthenticationError(
                        message="Failed to authenticate with Kimi API",
                        code=ErrorCode.UNAUTHENTICATED
                    )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise LLMAuthenticationError(
                    message="Failed to authenticate with Kimi API",
                    code=ErrorCode.UNAUTHENTICATED
                )
            raise LLMError(f"HTTP error while checking Kimi API key: {e}")
        except Exception as e:
            raise LLMError(f"Error while checking Kimi API key: {e}")

    async def _get_models_async(self) -> list[dict]:
        """获取Kimi模型列表，增加更详细的错误处理"""
        if not self.api_key:
            raise ValueError("No API key provided")
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=headers,
                    timeout=30.0  # 增加超时时间
                )
                
                # 更详细的错误处理
                if response.status_code == 401:
                    raise LLMAuthenticationError(
                        message="Kimi API密钥无效或已过期，请检查您的KIMI_API_KEY设置",
                        code=ErrorCode.UNAUTHENTICATED
                    )
                elif response.status_code == 403:
                    raise LLMPermissionDeniedError(
                        message="Kimi API访问被拒绝，请检查您的API密钥权限",
                        code=ErrorCode.PERMISSION_DENIED
                    )
                
                response.raise_for_status()
                data = response.json()
                return data.get("data", [])
        except httpx.TimeoutException:
            raise LLMTimeoutError(
                message="请求Kimi API超时，请检查网络连接",
                code=ErrorCode.TIMEOUT
            )
        except httpx.HTTPStatusError as e:
            raise LLMError(f"HTTP错误: {e}")
        except Exception as e:
            raise LLMError(f"获取Kimi模型时发生错误: {e}")

    async def list_llm_models_async(self) -> List[LLMConfig]:
        """Async version of listing Kimi models"""
        try:
            # Try to get models from API first
            models_data = await self._get_models_async()
            return self._list_llm_models(models_data)
        except Exception as e:
            # Fallback to hardcoded models if API fails
            import warnings
            warnings.warn(f"Failed to fetch Kimi models from API, using hardcoded list: {e}")
            return self._list_llm_models_hardcoded()

    def _list_llm_models(self, models_data: list) -> List[LLMConfig]:
        """Process models from API response"""
        configs = []
        for model in models_data:
            # Filter for Kimi models only
            model_id = model.get("id", "")
            if not (model_id.startswith("moonshot-") or model_id.startswith("kimi-")):
                continue
                
            model_name = model["id"]
            # Kimi API returns context_length in the model object
            context_window = model.get("context_length", 8192)  # Default to 8k if not specified
            
            # For newer Kimi K2 models, we may need to adjust put_inner_thoughts_in_kwargs
            put_inner_thoughts_in_kwargs = True
            # For K2 series models, set put_inner_thoughts_in_kwargs to False as they may have different behavior
            # For all Kimi models, we should set put_inner_thoughts_in_kwargs to False to ensure proper tool calling
            if "k2" in model_name.lower() or "thinking" in model_name.lower():
                put_inner_thoughts_in_kwargs = False
            # Also set to False for all Kimi models to ensure proper tool calling behavior
            elif model_name.startswith("kimi-") or model_name.startswith("moonshot-"):
                put_inner_thoughts_in_kwargs = False
                
            # Set max_reasoning_tokens for K2 series models
            max_reasoning_tokens = 0
            if "k2" in model_name.lower() or "thinking" in model_name.lower():
                max_reasoning_tokens = 1024
                
            configs.append(
                LLMConfig(
                    model=model_name,
                    model_endpoint_type="kimi",
                    model_endpoint=self.base_url,
                    context_window=context_window,
                    handle=self.get_handle(model_name),
                    provider_name=self.name,
                    provider_category=self.provider_category,
                    model_wrapper=None,
                    put_inner_thoughts_in_kwargs=put_inner_thoughts_in_kwargs,
                    temperature=0.7,
                    max_tokens=None,
                    enable_reasoner=True,
                    reasoning_effort=None,
                    max_reasoning_tokens=max_reasoning_tokens,
                    frequency_penalty=None,
                    compatibility_type=None,
                    verbosity=None,
                    tier=None,
                )
            )
        
        # If no models were found via API, fallback to hardcoded list
        if not configs:
            return self._list_llm_models_hardcoded()
            
        return configs

    def _list_llm_models_hardcoded(self) -> List[LLMConfig]:
        """List available Kimi models with their configurations (fallback)"""
        # Kimi models with their context window sizes
        kimi_models = {
            "moonshot-v1-8k": 8192,
            "moonshot-v1-32k": 32768,
            "moonshot-v1-128k": 131072,
            "kimi-k2-0905-preview": 262144,  # 256K context
            "kimi-k2-0711-preview": 131072,  # 128K context
            "kimi-k2-turbo-preview": 262144,  # 256K context
            "kimi-thinking-preview": 131072,  # 128K context
            "kimi-latest": 131072,  # 128K context
        }
        
        configs = []
        for model_name, context_window in kimi_models.items():
            # For newer Kimi K2 models, we may need to adjust put_inner_thoughts_in_kwargs
            put_inner_thoughts_in_kwargs = True
            # For K2 series models, set put_inner_thoughts_in_kwargs to False as they may have different behavior
            # For all Kimi models, we should set put_inner_thoughts_in_kwargs to False to ensure proper tool calling
            if "k2" in model_name.lower() or "thinking" in model_name.lower():
                put_inner_thoughts_in_kwargs = False
            # Also set to False for all Kimi models to ensure proper tool calling behavior
            elif model_name.startswith("kimi-") or model_name.startswith("moonshot-"):
                put_inner_thoughts_in_kwargs = False
                
            # Set max_reasoning_tokens for K2 series models
            max_reasoning_tokens = 0
            if "k2" in model_name.lower() or "thinking" in model_name.lower():
                max_reasoning_tokens = 1024
                
            configs.append(
                LLMConfig(
                    model=model_name,
                    model_endpoint_type="kimi",
                    model_endpoint=self.base_url,
                    context_window=context_window,
                    handle=self.get_handle(model_name),
                    provider_name=self.name,
                    provider_category=self.provider_category,
                    model_wrapper=None,
                    put_inner_thoughts_in_kwargs=put_inner_thoughts_in_kwargs,
                    temperature=0.7,
                    max_tokens=None,
                    enable_reasoner=True,
                    reasoning_effort=None,
                    max_reasoning_tokens=max_reasoning_tokens,
                    frequency_penalty=None,
                    compatibility_type=None,
                    verbosity=None,
                    tier=None,
                )
            )
        
        return configs

    def list_llm_models(self) -> List[LLMConfig]:
        """List available Kimi models with their configurations"""
        import asyncio
        import warnings

        warnings.warn("list_llm_models is deprecated, use list_llm_models_async instead", DeprecationWarning, stacklevel=2)

        # Simplified asyncio handling - just use asyncio.run()
        # This works in most contexts and avoids complex event loop detection
        try:
            return asyncio.run(self.list_llm_models_async())
        except RuntimeError as e:
            # If we're in an active event loop context, use a thread pool
            if "cannot be called from a running event loop" in str(e):
                import concurrent.futures

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.list_llm_models_async())
                    return future.result()
            else:
                raise

    async def list_embedding_models_async(self) -> List[EmbeddingConfig]:
        """Async version of listing Kimi embedding models"""
        # Kimi currently doesn't have dedicated embedding models
        # Using default embedding models
        return []

    def list_embedding_models(self) -> List[EmbeddingConfig]:
        """List available Kimi embedding models"""
        import asyncio
        import warnings

        warnings.warn("list_embedding_models is deprecated, use list_embedding_models_async instead", DeprecationWarning, stacklevel=2)

        # Simplified asyncio handling - just use asyncio.run()
        # This works in most contexts and avoids complex event loop detection
        try:
            return asyncio.run(self.list_embedding_models_async())
        except RuntimeError as e:
            # If we're in an active event loop context, use a thread pool
            if "cannot be called from a running event loop" in str(e):
                import concurrent.futures

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self.list_embedding_models_async())
                    return future.result()
            else:
                raise

    def get_handle(self, model_name: str, is_embedding: bool = False, base_name: Optional[str] = None) -> str:
        """Generate handle for the model"""
        model = model_name.split("/")[-1] if "/" in model_name else model_name
        return f"{self.name}/{model}"