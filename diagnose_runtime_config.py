#!/usr/bin/env python3
"""
诊断运行时配置的脚本
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


def check_runtime_environment():
    """检查运行时环境"""
    print("=== 运行时环境检查 ===")
    
    # 检查所有相关的环境变量
    relevant_vars = [
        'KIMI_API_KEY', 'LETTA_DISABLE_KIMI_PROVIDER',
        'ZHIPU_API_KEY', 'LETTA_DISABLE_ZHIPU_PROVIDER'
    ]
    
    for var in relevant_vars:
        value = os.environ.get(var, '未设置')
        # 对于API密钥，隐藏实际值
        if 'KEY' in var and value != '未设置':
            value = f"{'*' * (len(value)-8)}{value[-8:]}" if len(value) > 8 else '*' * len(value)
        print(f"  {var}: {value}")


def check_model_settings():
    """检查模型设置"""
    print("\n=== 模型设置检查 ===")
    
    print(f"Kimi API密钥: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"Kimi Base URL: {model_settings.kimi_base_url}")
    print(f"Zhipu API密钥: {'已设置' if model_settings.zhipu_api_key else '未设置'}")
    print(f"Zhipu Base URL: {model_settings.zhipu_base_url}")


def check_agent_configuration():
    """检查智能体配置"""
    print("\n=== 智能体配置检查 ===")
    
    try:
        # 创建服务器实例
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 获取默认用户
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        print(f"✅ 获取默认用户: {default_user.id}")
        
        # 使用您提供的agent ID进行检查
        agent_id = "agent-de6786cd-a467-4dae-acd8-43fb20ec8955"
        
        # 检查智能体配置
        try:
            agent = server.agent_manager.get_agent_by_id(agent_id=agent_id, actor=default_user)
            print(f"✅ 智能体存在: {agent.name}")
            print(f"  ID: {agent.id}")
            print(f"  模型: {agent.llm_config.model}")
            print(f"  提供商: {agent.llm_config.provider_name}")
            print(f"  Base URL: {agent.llm_config.model_endpoint}")
            
            # 检查提供商配置
            providers = server.get_enabled_providers(actor=default_user)
            kimi_provider = None
            for provider in providers:
                if provider.name == "kimi":
                    kimi_provider = provider
                    break
                    
            if kimi_provider:
                print(f"  Kimi提供商API密钥: {'已设置' if kimi_provider.api_key else '未设置'}")
                print(f"  Kimi提供商Base URL: {kimi_provider.base_url}")
            else:
                print("  ❌ 未找到Kimi提供商")
                
        except Exception as e:
            print(f"❌ 未找到智能体: {e}")
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()


def compare_configurations():
    """比较配置"""
    print("\n=== 配置比较 ===")
    
    # 比较model_settings和实际使用的配置
    print("Model settings中的Kimi配置:")
    print(f"  API密钥: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"  Base URL: {model_settings.kimi_base_url}")
    
    # 检查服务器中的提供商配置
    try:
        server = SyncServer()
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        
        providers = server.get_enabled_providers(actor=default_user)
        kimi_provider = None
        for provider in providers:
            if provider.name == "kimi":
                kimi_provider = provider
                break
                
        if kimi_provider:
            print("服务器中Kimi提供商配置:")
            print(f"  API密钥: {'已设置' if kimi_provider.api_key else '未设置'}")
            print(f"  Base URL: {kimi_provider.base_url}")
            
            # 比较配置是否一致
            if (model_settings.kimi_api_key == kimi_provider.api_key and 
                model_settings.kimi_base_url == kimi_provider.base_url):
                print("✅ 配置一致")
            else:
                print("❌ 配置不一致")
        else:
            print("❌ 服务器中未启用Kimi提供商")
            
    except Exception as e:
        print(f"❌ 配置比较失败: {e}")


def main():
    """主函数"""
    print("运行时配置诊断")
    print("=" * 20)
    
    # 检查运行时环境
    check_runtime_environment()
    
    # 检查模型设置
    check_model_settings()
    
    # 检查智能体配置
    check_agent_configuration()
    
    # 比较配置
    compare_configurations()
    
    print("\n" + "=" * 20)
    print("诊断完成。请检查以上信息以确定401错误的原因。")


if __name__ == "__main__":
    main()