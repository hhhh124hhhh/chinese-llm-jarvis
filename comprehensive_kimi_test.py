#!/usr/bin/env python3
"""
全面测试Kimi API集成
"""

import os
from letta.settings import model_settings
from letta.llm_api.kimi_client import KimiClient
from letta.schemas.llm_config import LLMConfig
from letta.schemas.enums import LLMConfigDefaults

def test_comprehensive_kimi():
    print("=== 全面测试Kimi API集成 ===")
    
    # 1. 检查API密钥加载
    print("\n1. 检查API密钥加载:")
    print(f"  model_settings.kimi_api_key: {repr(model_settings.kimi_api_key)}")
    print(f"  model_settings.kimi_base_url: {repr(model_settings.kimi_base_url)}")
    
    if not model_settings.kimi_api_key:
        print("❌ 未找到Kimi API密钥")
        return
    
    # 2. 测试KimiClient实例化
    print("\n2. 测试KimiClient实例化:")
    try:
        kimi_client = KimiClient()
        print("✅ KimiClient实例化成功")
    except Exception as e:
        print(f"❌ KimiClient实例化失败: {e}")
        return
    
    # 3. 测试_prepare_client_kwargs方法
    print("\n3. 测试_prepare_client_kwargs方法:")
    try:
        llm_config = LLMConfig(
            model="kimi-k2-0905-preview",
            model_endpoint=model_settings.kimi_base_url,
            model_endpoint_type="kimi",
            context_window=LLMConfigDefaults.CONTEXT_WINDOW,
            put_inner_thoughts_in_kwargs=LLMConfigDefaults.PUT_INNER_THOUGHTS_IN_KWARGS
        )
        client_kwargs = kimi_client._prepare_client_kwargs(llm_config)
        print("✅ _prepare_client_kwargs方法调用成功")
        print(f"  api_key长度: {len(client_kwargs.get('api_key', ''))}")
        print(f"  base_url: {client_kwargs.get('base_url', 'N/A')}")
    except Exception as e:
        print(f"❌ _prepare_client_kwargs方法调用失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. 测试API调用
    print("\n4. 测试API调用:")
    try:
        # 获取模型列表
        models = kimi_client.get_model_list(llm_config)
        print("✅ 获取模型列表成功")
        print(f"  可用模型数量: {len(models) if models else 0}")
        
        # 测试聊天完成
        from letta.schemas.message import Message, MessageRole
        from letta.schemas.letta_message_content import TextContent
        
        messages = [
            Message(
                role=MessageRole.user,
                content=[TextContent(text="你好，Kimi!")]
            )
        ]
        
        response = kimi_client.send_llm_request(
            llm_config=llm_config,
            messages=messages,
            tool_choice=None,
            tools=None,
            stream=False
        )
        print("✅ 聊天完成请求成功")
        print(f"  响应类型: {type(response)}")
        if hasattr(response, 'choices') and response.choices:
            print(f"  响应内容: {response.choices[0].message.content[:100]}...")
        
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_comprehensive_kimi()