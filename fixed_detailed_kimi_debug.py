#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正后的详细调试Kimi API密钥传递过程
"""
import os
import sys
from typing import Optional

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from letta.settings import model_settings
from letta.server.server import SyncServer
from letta.schemas.llm_config import LLMConfig
from letta.llm_api.kimi_client import KimiClient
from letta.services.user_manager import UserManager

def debug_model_settings():
    """调试ModelSettings中的Kimi配置"""
    print("=== ModelSettings调试 ===")
    print(f"model_settings.kimi_api_key: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    if model_settings.kimi_api_key:
        print(f"  API密钥长度: {len(model_settings.kimi_api_key)}")
        print(f"  API密钥前缀: {model_settings.kimi_api_key[:8]}...")
    
    print(f"model_settings.kimi_base_url: {model_settings.kimi_base_url}")
    print(f"os.environ.get('KIMI_API_KEY'): {'已设置' if os.environ.get('KIMI_API_KEY') else '未设置'}")
    if os.environ.get('KIMI_API_KEY'):
        env_key = os.environ.get('KIMI_API_KEY')
        print(f"  环境变量API密钥长度: {len(env_key)}")
        print(f"  环境变量API密钥前缀: {env_key[:8]}...")

def debug_server_kimi_provider():
    """调试服务器中的Kimi提供商配置"""
    print("\n=== 服务器Kimi提供商调试 ===")
    try:
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 查找Kimi提供商
        kimi_provider = None
        for provider in server._enabled_providers:
            if provider.name == "kimi":
                kimi_provider = provider
                break
        
        if kimi_provider:
            print("✅ 找到Kimi提供商")
            print(f"  提供商名称: {kimi_provider.name}")
            print(f"  提供商类型: {kimi_provider.provider_type}")
            print(f"  API密钥: {'已设置' if kimi_provider.api_key else '未设置'}")
            if kimi_provider.api_key:
                print(f"    API密钥长度: {len(kimi_provider.api_key)}")
                print(f"    API密钥前缀: {kimi_provider.api_key[:8]}...")
            print(f"  Base URL: {kimi_provider.base_url}")
        else:
            print("❌ 未找到Kimi提供商")
            
    except Exception as e:
        print(f"❌ 服务器Kimi提供商调试失败: {e}")
        import traceback
        traceback.print_exc()

def debug_kimi_client_preparation():
    """调试KimiClient参数准备过程"""
    print("\n=== KimiClient参数准备调试 ===")
    
    # 创建一个模拟的LLMConfig
    llm_config = LLMConfig(
        model="kimi-k2-0905-preview",
        model_endpoint_type="openai",
        model_endpoint="https://api.moonshot.cn/v1",
        context_window=32768,
        provider_name="kimi",
        provider_category="base"
    )
    
    print("LLM配置详情:")
    print(f"  model: {llm_config.model}")
    print(f"  model_endpoint_type: {llm_config.model_endpoint_type}")
    print(f"  model_endpoint: {llm_config.model_endpoint}")
    print(f"  provider_name: {llm_config.provider_name}")
    print(f"  provider_category: {llm_config.provider_category}")
    
    try:
        # 创建KimiClient实例
        kimi_client = KimiClient()
        print("✅ KimiClient实例创建成功")
        
        # 调用_prepare_client_kwargs方法
        client_kwargs = kimi_client._prepare_client_kwargs(llm_config)
        print("✅ _prepare_client_kwargs调用成功")
        print(f"  api_key: {'已设置' if client_kwargs.get('api_key') else '未设置'}")
        if client_kwargs.get('api_key'):
            print(f"    API密钥长度: {len(client_kwargs['api_key'])}")
            print(f"    API密钥前缀: {client_kwargs['api_key'][:8]}...")
        print(f"  base_url: {client_kwargs.get('base_url')}")
        
    except Exception as e:
        print(f"❌ KimiClient参数准备调试失败: {e}")
        import traceback
        traceback.print_exc()

def debug_actual_request():
    """调试实际请求过程"""
    print("\n=== 实际请求调试 ===")
    
    try:
        # 获取默认用户和智能体
        server = SyncServer()
        user_manager = UserManager()
        user = user_manager.get_default_user()
        print(f"✅ 获取默认用户: {user.id}")
        
        # 获取智能体
        agents = server.agent_manager.list_agents(actor=user)
        agent = None
        for a in agents:
            if "personal-assistant" in a.name:
                agent = server.agent_manager.get_agent_by_id(agent_id=a.id, actor=user)
                break
                
        if not agent:
            print("❌ 未找到个人助理智能体")
            return
            
        print(f"✅ 找到智能体: {agent.name}")
        print(f"  模型: {agent.llm_config.model}")
        print(f"  提供商: {agent.llm_config.provider_name}")
        print(f"  Base URL: {agent.llm_config.model_endpoint}")
        
        # 创建KimiClient实例
        kimi_client = KimiClient()
        print("✅ KimiClient实例创建成功")
        
        # 准备请求数据
        messages = [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ]
        
        # 构建请求数据
        request_data = kimi_client.build_request_data(
            messages=messages,
            llm_config=agent.llm_config
        )
        print("✅ 请求数据构建成功")
        print(f"  模型: {request_data.get('model')}")
        print(f"  消息数量: {len(request_data.get('messages', []))}")
        
        # 准备客户端参数
        client_kwargs = kimi_client._prepare_client_kwargs(agent.llm_config)
        print("✅ 客户端参数准备成功")
        print(f"  API密钥: {'已设置' if client_kwargs.get('api_key') else '未设置'}")
        if client_kwargs.get('api_key'):
            print(f"    API密钥长度: {len(client_kwargs['api_key'])}")
            print(f"    API密钥前缀: {client_kwargs['api_key'][:8]}...")
        print(f"  Base URL: {client_kwargs.get('base_url')}")
        
        # 尝试发送请求（但不真正发送，只检查参数）
        print("✅ 准备就绪，可以发送请求")
        
    except Exception as e:
        print(f"❌ 实际请求调试失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("Kimi API密钥传递详细调试（修正版）")
    print("=" * 40)
    
    debug_model_settings()
    debug_server_kimi_provider()
    debug_kimi_client_preparation()
    debug_actual_request()
    
    print("\n" + "=" * 40)
    print("调试完成。请检查以上信息以确定401错误的原因。")

if __name__ == "__main__":
    main()