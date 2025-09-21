#!/usr/bin/env python3
"""
测试Kimi模型的脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.settings import model_settings
from letta.server.server import SyncServer
from letta.schemas.enums import ProviderType, ProviderCategory
from letta.schemas.providers import KimiProvider
from letta.schemas.llm_config import LLMConfig


def test_kimi_provider():
    """测试Kimi提供商"""
    print("=== 测试Kimi提供商 ===")
    
    try:
        # 创建Kimi提供商实例
        kimi_provider = KimiProvider(
            name="kimi",
            provider_type=ProviderType.kimi,
            provider_category=ProviderCategory.base,
            api_key=model_settings.kimi_api_key,
            base_url=model_settings.kimi_base_url,
            id=None,
            access_key=None,
            region=None,
            api_version=None,
            organization_id=None,
            updated_at=None
        )
        print("✅ Kimi提供商实例创建成功")
        
        # 列出模型
        models = kimi_provider.list_llm_models()
        print(f"✅ 可用模型数量: {len(models)}")
        
        # 显示前几个模型
        print("前3个模型:")
        for model in models[:3]:
            print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
            
        return kimi_provider, models
        
    except Exception as e:
        print(f"❌ Kimi提供商测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None, []


def test_create_agent_with_kimi():
    """测试使用Kimi模型创建智能体"""
    print("\n=== 测试使用Kimi模型创建智能体 ===")
    
    try:
        # 创建服务器实例
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 检查Kimi提供商是否已启用
        kimi_enabled = any(provider.name == "kimi" for provider in server._enabled_providers)
        if kimi_enabled:
            print("✅ Kimi提供商已启用")
        else:
            print("❌ Kimi提供商未启用")
            return False
            
        # 获取默认用户
        from letta.orm.users import User as OrmUser
        from letta.services.user_manager import UserManager
        
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        print(f"✅ 获取默认用户: {default_user.id}")
        
        # 创建智能体请求
        from letta.schemas.agent import CreateAgent
        
        agent_request = CreateAgent(
            name="test_kimi_agent",
            model="kimi/moonshot-v1-128k",  # 使用Kimi模型
        )
        
        print("正在创建智能体...")
        # 创建智能体
        agent_state = server.create_agent(
            request=agent_request,
            actor=default_user
        )
        
        print(f"✅ 智能体创建成功: {agent_state.name} (ID: {agent_state.id})")
        print(f"使用的模型: {agent_state.llm_config.model}")
        print(f"提供商: {agent_state.llm_config.provider_name}")
        
        return agent_state
        
    except Exception as e:
        print(f"❌ 创建智能体失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    print("Kimi模型测试")
    print("=" * 30)
    
    # 测试Kimi提供商
    provider, models = test_kimi_provider()
    
    if provider and models:
        # 测试创建智能体
        agent_state = test_create_agent_with_kimi()
        
        if agent_state:
            print("\n🎉 所有测试通过! Kimi模型可以正常使用。")
        else:
            print("\n❌ 智能体创建失败，请检查配置。")
    else:
        print("\n❌ Kimi提供商测试失败，请检查API密钥配置。")


if __name__ == "__main__":
    main()