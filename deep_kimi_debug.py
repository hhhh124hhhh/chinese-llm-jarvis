#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深入调试Kimi API密钥传递过程
"""
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from letta.settings import model_settings
from letta.server.server import SyncServer
from letta.schemas.llm_config import LLMConfig
from letta.llm_api.kimi_client import KimiClient
from letta.services.user_manager import UserManager

def debug_environment():
    """调试环境变量"""
    print("=== 环境变量调试 ===")
    print(f"KIMI_API_KEY环境变量: {'已设置' if os.environ.get('KIMI_API_KEY') else '未设置'}")
    if os.environ.get('KIMI_API_KEY'):
        env_key = os.environ.get('KIMI_API_KEY')
        print(f"  长度: {len(env_key)}")
        print(f"  前缀: {env_key[:10]}...")
    
    print(f"model_settings.kimi_api_key: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    if model_settings.kimi_api_key:
        print(f"  长度: {len(model_settings.kimi_api_key)}")
        print(f"  前缀: {model_settings.kimi_api_key[:10]}...")

def debug_server_providers():
    """调试服务器提供商配置"""
    print("\n=== 服务器提供商调试 ===")
    server = SyncServer()
    
    print("所有启用的提供商:")
    for provider in server._enabled_providers:
        print(f"  - {provider.name} ({provider.provider_type})")
        if provider.name == "kimi":
            print(f"    API密钥: {'已设置' if provider.api_key else '未设置'}")
            if provider.api_key:
                print(f"    API密钥长度: {len(provider.api_key)}")
                print(f"    API密钥前缀: {provider.api_key[:10]}...")
            print(f"    Base URL: {provider.base_url}")

def debug_kimi_client_direct():
    """直接调试KimiClient"""
    print("\n=== 直接调试KimiClient ===")
    
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
        provider_category="base"
    )
    
    print("LLM配置:")
    print(f"  model: {llm_config.model}")
    print(f"  model_endpoint: {llm_config.model_endpoint}")
    print(f"  provider_name: {llm_config.provider_name}")
    
    # 调用_prepare_client_kwargs方法
    try:
        client_kwargs = kimi_client._prepare_client_kwargs(llm_config)
        print("✅ _prepare_client_kwargs调用成功")
        print(f"  api_key: {'已设置' if client_kwargs.get('api_key') else '未设置'}")
        if client_kwargs.get('api_key'):
            print(f"    长度: {len(client_kwargs['api_key'])}")
            print(f"    前缀: {client_kwargs['api_key'][:10]}...")
        print(f"  base_url: {client_kwargs.get('base_url')}")
    except Exception as e:
        print(f"❌ _prepare_client_kwargs调用失败: {e}")
        import traceback
        traceback.print_exc()

def debug_agent_llm_config():
    """调试智能体的LLM配置"""
    print("\n=== 智能体LLM配置调试 ===")
    
    # 获取服务器和用户
    server = SyncServer()
    user_manager = UserManager()
    user = user_manager.get_default_user()
    print(f"✅ 获取默认用户: {user.id}")
    
    # 获取智能体
    agents = server.agent_manager.list_agents(actor=user)
    print(f"总共找到 {len(agents)} 个智能体")
    
    # 查找使用Kimi的智能体
    kimi_agents = [agent for agent in agents if agent.llm_config.provider_name == "kimi"]
    print(f"找到 {len(kimi_agents)} 个使用Kimi的智能体")
    
    for i, agent in enumerate(kimi_agents[:2]):  # 只检查前两个
        print(f"\n智能体 {i+1}: {agent.name}")
        print(f"  ID: {agent.id}")
        print(f"  模型: {agent.llm_config.model}")
        print(f"  提供商: {agent.llm_config.provider_name}")
        print(f"  Base URL: {agent.llm_config.model_endpoint}")
        print(f"  Handle: {agent.llm_config.handle}")

def main():
    """主函数"""
    print("Kimi API密钥传递深入调试")
    print("=" * 50)
    
    debug_environment()
    debug_server_providers()
    debug_kimi_client_direct()
    debug_agent_llm_config()
    
    print("\n" + "=" * 50)
    print("调试完成！")

if __name__ == "__main__":
    main()