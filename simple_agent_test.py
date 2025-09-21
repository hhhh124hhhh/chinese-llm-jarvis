#!/usr/bin/env python3
"""
简单的智能体测试脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.server.server import SyncServer
from letta.services.user_manager import UserManager


def test_agent_exists():
    """测试智能体是否存在"""
    print("=== 测试智能体是否存在 ===")
    
    try:
        # 创建服务器实例
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 获取默认用户
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        print(f"✅ 获取默认用户: {default_user.id}")
        
        # 使用您提供的agent ID进行测试
        agent_id = "agent-de6786cd-a467-4dae-acd8-43fb20ec8955"
        
        # 检查智能体是否存在
        try:
            agent = server.agent_manager.get_agent_by_id(agent_id=agent_id, actor=default_user)
            print(f"✅ 智能体存在: {agent.name}")
            print(f"  ID: {agent.id}")
            print(f"  模型: {agent.llm_config.model}")
            print(f"  提供商: {agent.llm_config.provider_name}")
            return True
        except Exception as e:
            print(f"❌ 未找到智能体: {e}")
            return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("简单智能体测试")
    print("=" * 20)
    
    success = test_agent_exists()
    
    if success:
        print("\n🎉 智能体存在且配置正确!")
    else:
        print("\n❌ 智能体测试失败")


if __name__ == "__main__":
    main()