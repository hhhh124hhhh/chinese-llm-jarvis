#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实际的Kimi API请求
"""
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

import httpx
from letta.settings import model_settings
from letta.server.server import SyncServer
from letta.schemas.llm_config import LLMConfig
from letta.llm_api.kimi_client import KimiClient
from letta.services.user_manager import UserManager
from letta.schemas.message import Message as PydanticMessage
from letta.schemas.letta_message_content import TextContent
from letta.schemas.enums import MessageRole, ProviderCategory

def test_direct_kimi_api_call():
    """直接测试Kimi API调用"""
    print("=== 直接测试Kimi API调用 ===")
    
    # 获取API密钥并清理空格
    api_key = model_settings.kimi_api_key or os.environ.get("KIMI_API_KEY")
    if not api_key:
        print("❌ 未找到API密钥")
        return False
        
    # 清理API密钥末尾的空格
    api_key = api_key.strip()
    print(f"✅ API密钥已找到，长度: {len(api_key)}")
    
    # 构造请求
    url = "https://api.moonshot.cn/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print(f"请求URL: {url}")
    print(f"请求头Authorization前缀: Bearer {api_key[:10]}...")
    
    try:
        response = httpx.get(url, headers=headers, timeout=30.0)
        print(f"✅ HTTP请求成功")
        print(f"  状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  可用模型数量: {len(data.get('data', []))}")
        else:
            print(f"  错误响应: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ HTTP请求失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_kimi_client_request():
    """测试KimiClient请求"""
    print("\n=== 测试KimiClient请求 ===")
    
    try:
        # 创建KimiClient实例
        kimi_client = KimiClient()
        print("✅ KimiClient实例创建成功")
        
        # 创建LLM配置
        llm_config = LLMConfig(
            model="kimi-k2-0905-preview",
            model_endpoint_type="openai",
            model_endpoint="https://api.moonshot.cn/v1",
            context_window=32768,
            provider_name="kimi",
            provider_category=ProviderCategory.base,
            model_wrapper=None,
            put_inner_thoughts_in_kwargs=True,
            handle="kimi/kimi-k2-0905-preview",
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
        
        print("LLM配置:")
        print(f"  model: {llm_config.model}")
        print(f"  model_endpoint: {llm_config.model_endpoint}")
        
        # 准备客户端参数
        client_kwargs = kimi_client._prepare_client_kwargs(llm_config)
        print("✅ 客户端参数准备成功")
        api_key = client_kwargs.get('api_key')
        base_url = client_kwargs.get('base_url')
        print(f"  api_key: {api_key[:10] if api_key else '未设置'}...")
        print(f"  base_url: {base_url}")
        
        # 构造正确的消息对象
        messages = [
            PydanticMessage(
                role=MessageRole.user,
                content=[TextContent(text="你好，请介绍一下你自己")]
            )
        ]
        
        # 构造请求数据
        request_data = kimi_client.build_request_data(
            messages=messages,
            llm_config=llm_config
        )
        print("✅ 请求数据构建成功")
        print(f"  模型: {request_data.get('model')}")
        print(f"  消息数量: {len(request_data.get('messages', []))}")
        
        # 尝试发送请求（使用httpx直接发送以避免OpenAI客户端的复杂性）
        api_key = api_key.strip() if api_key else None
        base_url = base_url
        
        if not api_key or not base_url:
            print("❌ API密钥或Base URL缺失")
            return False
            
        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": request_data.get('model'),
            "messages": request_data.get('messages'),
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        print(f"请求URL: {url}")
        print(f"请求头Authorization前缀: Bearer {api_key[:10]}...")
        print(f"请求体模型: {payload['model']}")
        
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        print(f"✅ HTTP请求完成")
        print(f"  状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"  响应: {response.json()}")
            return True
        else:
            print(f"  错误响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ KimiClient请求测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("Kimi API实际请求测试")
    print("=" * 50)
    
    # 测试直接API调用
    direct_success = test_direct_kimi_api_call()
    
    # 测试KimiClient请求
    client_success = test_kimi_client_request()
    
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"  直接API调用: {'✅ 成功' if direct_success else '❌ 失败'}")
    print(f"  KimiClient请求: {'✅ 成功' if client_success else '❌ 失败'}")
    
    if direct_success and not client_success:
        print("\n💡 注意: 直接API调用成功但KimiClient请求失败，说明问题可能在KimiClient的实现中")

if __name__ == "__main__":
    main()