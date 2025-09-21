#!/usr/bin/env python3
"""
简单测试Kimi API密钥传递
"""

import os
from letta.settings import model_settings
from letta.llm_api.kimi_client import KimiClient
from letta.schemas.llm_config import LLMConfig

def test_simple_kimi():
    print("=== 简单测试Kimi API密钥传递 ===")
    
    # 1. 检查API密钥
    print(f"model_settings.kimi_api_key: {repr(model_settings.kimi_api_key)}")
    
    # 2. 创建KimiClient实例
    kimi_client = KimiClient()
    print("✅ KimiClient实例创建成功")
    
    # 3. 创建简单的LLMConfig，使用openai类型因为Kimi兼容OpenAI API
    llm_config = LLMConfig(
        model="kimi-k2-0905-preview",
        model_endpoint_type="openai",  # Kimi兼容OpenAI API
        model_endpoint=model_settings.kimi_base_url,
        context_window=32768,
        put_inner_thoughts_in_kwargs=True,
        provider_name="kimi",
        provider_category=None,
        model_wrapper=None,
        handle=None,
        temperature=0.7,
        max_tokens=None,
        enable_reasoner=True,
        reasoning_effort=None,
        max_reasoning_tokens=0,
        frequency_penalty=None,
        compatibility_type=None,
        verbosity=None,
        tier=None
    )
    print("✅ LLMConfig创建成功")
    
    # 4. 测试_prepare_client_kwargs方法
    client_kwargs = kimi_client._prepare_client_kwargs(llm_config)
    print("✅ _prepare_client_kwargs调用成功")
    print(f"  api_key: {client_kwargs.get('api_key', 'N/A')[:10]}...")
    print(f"  base_url: {client_kwargs.get('base_url', 'N/A')}")
    
    # 5. 验证API密钥是否正确
    api_key = client_kwargs.get('api_key', '')
    if api_key == model_settings.kimi_api_key:
        print("✅ API密钥正确传递")
    else:
        print("❌ API密钥传递错误")
        print(f"  期望: {repr(model_settings.kimi_api_key)}")
        print(f"  实际: {repr(api_key)}")

if __name__ == "__main__":
    test_simple_kimi()