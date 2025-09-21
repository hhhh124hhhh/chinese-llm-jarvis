#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终调试Kimi 401错误
"""
import os
import sys
import traceback

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from letta.settings import model_settings
from letta.server.server import SyncServer
from letta.schemas.llm_config import LLMConfig
from letta.llm_api.kimi_client import KimiClient
from letta.services.user_manager import UserManager
from letta.schemas.agent import CreateAgent
from letta.schemas.message import MessageCreate
from letta.schemas.letta_message_content import TextContent
from letta.schemas.enums import MessageRole, ProviderCategory

def debug_kimi_401_error():
    """调试Kimi 401错误的根本原因"""
    print("=== 调试Kimi 401错误 ===")
    
    # 1. 检查环境变量和ModelSettings
    print("1. 检查环境变量和ModelSettings配置:")
    print(f"   model_settings.kimi_api_key: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"   os.environ.get('KIMI_API_KEY'): {'已设置' if os.environ.get('KIMI_API_KEY') else '未设置'}")
    
    if model_settings.kimi_api_key:
        print(f"   model_settings API密钥长度: {len(model_settings.kimi_api_key)}")
        print(f"   model_settings API密钥前缀: {model_settings.kimi_api_key[:10]}...")
        
    if os.environ.get('KIMI_API_KEY'):
        env_key = os.environ.get('KIMI_API_KEY')
        print(f"   环境变量API密钥长度: {len(env_key)}")
        print(f"   环境变量API密钥前缀: {env_key[:10]}...")
    
    # 2. 检查服务器中的Kimi提供商配置
    print("\n2. 检查服务器中的Kimi提供商配置:")
    try:
        server = SyncServer()
        kimi_provider = None
        for provider in server._enabled_providers:
            if provider.name == "kimi":
                kimi_provider = provider
                break
                
        if kimi_provider:
            print("   ✅ 找到Kimi提供商")
            print(f"   提供商API密钥: {'已设置' if kimi_provider.api_key else '未设置'}")
            if kimi_provider.api_key:
                print(f"   提供商API密钥长度: {len(kimi_provider.api_key)}")
                print(f"   提供商API密钥前缀: {kimi_provider.api_key[:10]}...")
            print(f"   提供商Base URL: {kimi_provider.base_url}")
        else:
            print("   ❌ 未找到Kimi提供商")
            return False
    except Exception as e:
        print(f"   ❌ 检查服务器Kimi提供商失败: {e}")
        traceback.print_exc()
        return False
    
    # 3. 直接测试Kimi API密钥
    print("\n3. 直接测试Kimi API密钥:")
    try:
        kimi_client = KimiClient()
        
        # 创建一个简单的LLM配置用于测试
        test_llm_config = LLMConfig(
            model="kimi-k2-0905-preview",
            model_endpoint_type="openai",
            model_endpoint="https://api.moonshot.cn/v1",
            context_window=32768,
            provider_name="kimi",
            provider_category=ProviderCategory.base,
            handle="kimi/kimi-k2-0905-preview",
            temperature=0.7,
            model_wrapper=None,
            put_inner_thoughts_in_kwargs=True,
            max_tokens=None,
            enable_reasoner=True,
            max_reasoning_tokens=0,
            frequency_penalty=None,
            compatibility_type=None,
            verbosity=None,
            tier=None,
            reasoning_effort=None,
        )
        
        # 准备客户端参数
        client_kwargs = kimi_client._prepare_client_kwargs(test_llm_config)
        print("   ✅ 客户端参数准备成功")
        print(f"   准备的API密钥: {'已设置' if client_kwargs.get('api_key') else '未设置'}")
        if client_kwargs.get('api_key'):
            print(f"   准备的API密钥长度: {len(client_kwargs['api_key'])}")
            print(f"   准备的API密钥前缀: {client_kwargs['api_key'][:10]}...")
        print(f"   准备的Base URL: {client_kwargs.get('base_url')}")
        
        # 测试API密钥是否有效
        from openai import OpenAI
        test_client = OpenAI(api_key=client_kwargs['api_key'], base_url=client_kwargs['base_url'])
        models = test_client.models.list()
        print("   ✅ API密钥验证成功")
        print(f"   可用模型数量: {len(models.data)}")
        
    except Exception as e:
        print(f"   ❌ 直接测试Kimi API密钥失败: {e}")
        traceback.print_exc()
        return False
    
    # 4. 检查智能体配置
    print("\n4. 检查智能体配置:")
    try:
        user_manager = UserManager()
        user = user_manager.get_default_user()
        print(f"   ✅ 获取默认用户: {user.id}")
        
        # 获取现有的使用Kimi的智能体
        agents = server.agent_manager.list_agents(actor=user)
        kimi_agent = None
        for agent in agents:
            if agent.llm_config.provider_name == "kimi":
                kimi_agent = agent
                break
                
        if kimi_agent:
            print("   ✅ 找到使用Kimi的智能体")
            print(f"   智能体模型: {kimi_agent.llm_config.model}")
            print(f"   智能体Base URL: {kimi_agent.llm_config.model_endpoint}")
        else:
            print("   ⚠️  未找到使用Kimi的智能体")
            
    except Exception as e:
        print(f"   ❌ 检查智能体配置失败: {e}")
        traceback.print_exc()
        return False
    
    # 5. 总结
    print("\n=== 调试总结 ===")
    print("从以上调试信息可以看出:")
    print("1. API密钥在环境变量和ModelSettings中都已正确设置")
    print("2. Kimi提供商在服务器中已正确启用")
    print("3. 直接使用API密钥测试可以成功获取模型列表")
    print("4. 但在实际使用智能体时出现401错误")
    
    print("\n可能的原因:")
    print("1. 在实际请求过程中，API密钥没有被正确传递")
    print("2. 智能体的配置可能与服务器提供商配置不一致")
    print("3. 可能存在运行时环境问题，需要重启服务")
    
    print("\n建议解决方案:")
    print("1. 重启Letta服务以确保环境变量正确加载")
    print("2. 检查智能体的LLM配置是否与Kimi提供商配置一致")
    print("3. 如果问题仍然存在，尝试重新创建使用Kimi模型的智能体")
    
    return True

def main():
    print("Kimi 401错误最终调试")
    print("=" * 30)
    
    success = debug_kimi_401_error()
    
    if success:
        print("\n✅ 调试完成，请根据建议解决方案进行操作。")
    else:
        print("\n❌ 调试过程中出现错误，请检查以上信息。")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)