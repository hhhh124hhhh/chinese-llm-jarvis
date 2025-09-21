#!/usr/bin/env python3
"""
正确调试Kimi请求的脚本
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


def check_llm_config_and_provider():
    """检查LLM配置和提供商"""
    print("=== 检查LLM配置和提供商 ===")
    
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
        
        # 检查提供商配置
        providers = server.get_enabled_providers(actor=default_user)
        kimi_provider = None
        for provider in providers:
            if provider.name == "kimi":
                kimi_provider = provider
                break
                
        if kimi_provider:
            print(f"\nKimi提供商配置:")
            print(f"  name: {kimi_provider.name}")
            print(f"  provider_type: {kimi_provider.provider_type}")
            print(f"  provider_category: {kimi_provider.provider_category}")
            print(f"  base_url: {kimi_provider.base_url}")
            print(f"  API密钥状态: {'已设置' if kimi_provider.api_key else '未设置'}")
            if kimi_provider.api_key:
                print(f"  API密钥长度: {len(kimi_provider.api_key)}")
                print(f"  API密钥前缀: {kimi_provider.api_key[:10] if len(kimi_provider.api_key) > 10 else kimi_provider.api_key}")
        else:
            print(f"\n❌ 未找到Kimi提供商")
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()


def test_provider_api_key():
    """测试提供商API密钥"""
    print("\n=== 测试提供商API密钥 ===")
    
    try:
        server = SyncServer()
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        
        # 获取Kimi提供商
        providers = server.get_enabled_providers(actor=default_user)
        kimi_provider = None
        for provider in providers:
            if provider.name == "kimi":
                kimi_provider = provider
                break
                
        if not kimi_provider:
            print("❌ 未找到Kimi提供商")
            return
            
        if not kimi_provider.api_key:
            print("❌ Kimi提供商未设置API密钥")
            return
            
        # 测试API密钥
        import httpx
        
        url = f"{kimi_provider.base_url}/models"
        headers = {
            "Authorization": f"Bearer {kimi_provider.api_key}",
            "Content-Type": "application/json"
        }
        
        print("正在测试Kimi API密钥...")
        response = httpx.get(url, headers=headers, timeout=10.0)
        print(f"HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Kimi API密钥验证成功")
            data = response.json()
            print(f"可用模型数量: {len(data.get('data', []))}")
        elif response.status_code == 401:
            print("❌ Kimi API密钥验证失败 (401 Unauthorized)")
            print(f"错误信息: {response.text}")
        else:
            print(f"❌ 请求失败 (状态码: {response.status_code})")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("正确调试Kimi请求")
    print("=" * 20)
    
    # 检查LLM配置和提供商
    check_llm_config_and_provider()
    
    # 测试提供商API密钥
    test_provider_api_key()
    
    print("\n" + "=" * 20)
    print("调试完成。")


if __name__ == "__main__":
    main()