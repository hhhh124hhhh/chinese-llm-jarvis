import os
from typing import List, Optional

from letta.llm_api.llm_client_base import LLMClientBase
from letta.llm_api.openai_client import OpenAIClient
from letta.schemas.embedding_config import EmbeddingConfig
from letta.schemas.llm_config import LLMConfig
from letta.settings import model_settings
from letta.schemas.openai.chat_completion_request import ToolFunctionChoice
from letta.schemas.message import Message
from letta.schemas.openai.chat_completion_response import ChatCompletionResponse


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

    def build_request_data(
        self,
        messages: List[Message],
        llm_config: LLMConfig,
        tools: Optional[List[dict]] = None,
        force_tool_call: Optional[str] = None,
    ) -> dict:
        """Build request data for Kimi API with special handling for tool choice"""
        # Use the parent implementation but with special handling for Kimi models
        request_data = super().build_request_data(messages, llm_config, tools, force_tool_call)
        
        # For Kimi models, we may need to adjust tool choice behavior
        if tools and llm_config.model:
            # For K2 series models and thinking models, use "auto" tool choice
            if "k2" in llm_config.model.lower() or "thinking" in llm_config.model.lower():
                request_data["tool_choice"] = "auto"
            # For other Kimi models, ensure tool_choice is set to "required" if not already set
            elif "tool_choice" not in request_data or request_data["tool_choice"] is None:
                request_data["tool_choice"] = "required"
            
        # Log the request data for debugging purposes
        import json
        print(f"Kimi request data: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
            
        return request_data

    def requires_auto_tool_choice(self, llm_config: LLMConfig) -> bool:
        """Kimi may require auto tool choice for certain models"""
        # For newer Kimi models, especially K2 series, we may need to use "auto" tool choice
        if llm_config.model and ("k2" in llm_config.model.lower() or "thinking" in llm_config.model.lower()):
            return True
        return super().requires_auto_tool_choice(llm_config)

    def supports_structured_output(self, llm_config: LLMConfig) -> bool:
        """Kimi does not reliably support structured output"""
        # Kimi models do not reliably support structured output
        return False

    def convert_response_to_chat_completion(
        self,
        response_data: dict,
        input_messages: List[Message],
        llm_config: LLMConfig,
    ) -> ChatCompletionResponse:
        """Convert Kimi API response to ChatCompletionResponse with special handling"""
        # Use the parent implementation
        response = super().convert_response_to_chat_completion(response_data, input_messages, llm_config)
        
        # Log the response for debugging purposes
        import json
        print(f"Kimi response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        
        # Check if the response has tool calls
        if response.choices and response.choices[0].message:
            message = response.choices[0].message
            if not message.tool_calls:
                print("Warning: Kimi response does not contain tool calls")
            
        return response