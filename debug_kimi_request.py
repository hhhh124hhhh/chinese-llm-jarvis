#!/usr/bin/env python3
"""
调试Kimi请求的脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.settings import model_settings
from letta.server.server import SyncServer
from letta.services.user_manager import UserManager
from letta.llm_api.openai_client import OpenAIClient
from letta.schemas.llm_config import LLMConfig


def debug_kimi_request():
    """调试Kimi请求"""
    print("=== 调试Kimi请求 ===")
    
    # 获取智能体配置
    try:
        server = SyncServer()
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        
        agent_id = "agent-de6786cd-a467-4dae-acd8-43fb20ec8955"
        agent = server.agent_manager.get_agent_by_id(agent_id=agent_id, actor=default_user)
        
        print(f"智能体模型配置:")
        print(f"  模型: {agent.llm_config.model}")
        print(f"  提供商: {agent.llm_config.provider_name}")
        print(f"  Base URL: {agent.llm_config.model_endpoint}")
        print(f"  API密钥: {'已设置' if agent.llm_config.api_key else '未设置'}")
        
        # 创建OpenAI客户端
        client = OpenAIClient()
        print(f"✅ OpenAI客户端创建成功")
        
        # 构造请求数据
        request_data = {
            "model": agent.llm_config.model,
            "messages": [
                {"role": "user", "content": "你好，请介绍一下你自己"}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        print(f"请求数据:")
        print(f"  model: {request_data['model']}")
        print(f"  messages: {request_data['messages']}")
        
        # 尝试发送请求
        print(f"\n正在发送请求...")
        try:
            response = client.request(request_data, agent.llm_config)
            print(f"✅ 请求成功")
            print(f"响应: {response}")
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            print(f"错误类型: {type(e)}")
            
            # 检查错误详情
            if hasattr(e, 'response'):
                print(f"响应内容: {e.response.text}")
                
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()


def check_llm_config():
    """检查LLM配置"""
    print("\n=== 检查LLM配置 ===")
    
    try:
        server = SyncServer()
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        
        agent_id = "agent-de6786cd-a467-4dae-acd8-43fb20ec8955"
        agent = server.agent_manager.get_agent_by_id(agent_id=agent_id, actor=default_user)
        
        llm_config = agent.llm_config
        print(f"LLM配置详情:")
        print(f"  model: {llm_config.model}")
        print(f"  model_endpoint_type: {llm_config.model_endpoint_type}")
        print(f"  model_endpoint: {llm_config.model_endpoint}")
        print(f"  provider_name: {llm_config.provider_name}")
        print(f"  provider_category: {llm_config.provider_category}")
        print(f"  api_key: {'已设置' if llm_config.api_key else '未设置'}")
        
        # 检查API密钥是否在LLM配置中
        if llm_config.api_key:
            print(f"  API密钥长度: {len(llm_config.api_key)}")
            print(f"  API密钥前缀: {llm_config.api_key[:10] if len(llm_config.api_key) > 10 else llm_config.api_key}")
        else:
            print(f"  ⚠️  LLM配置中未设置API密钥，将使用提供商配置中的API密钥")
            
            # 检查提供商配置
            providers = server.get_enabled_providers(actor=default_user)
            kimi_provider = None
            for provider in providers:
                if provider.name == "kimi":
                    kimi_provider = provider
                    break
                    
            if kimi_provider and kimi_provider.api_key:
                print(f"  提供商API密钥长度: {len(kimi_provider.api_key)}")
                print(f"  提供商API密钥前缀: {kimi_provider.api_key[:10] if len(kimi_provider.api_key) > 10 else kimi_provider.api_key}")
            else:
                print(f"  ❌ 提供商中也未设置API密钥")
                
    except Exception as e:
        print(f"❌ 检查LLM配置失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("Kimi请求调试")
    print("=" * 20)
    
    # 检查LLM配置
    check_llm_config()
    
    # 调试Kimi请求
    debug_kimi_request()
    
    print("\n" + "=" * 20)
    print("调试完成。请检查以上信息以确定401错误的原因。")


if __name__ == "__main__":
    main()