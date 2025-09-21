#!/usr/bin/env python3
"""
修复Kimi智能体配置的脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.server.server import SyncServer
from letta.services.user_manager import UserManager
from letta.schemas.agent import UpdateAgent


def fix_kimi_agents():
    """修复使用letta-free模型的智能体，将其改为使用Kimi模型"""
    print("=== 修复Kimi智能体配置 ===")
    
    try:
        # 创建服务器实例
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 获取默认用户
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        print(f"✅ 获取默认用户: {default_user.id}")
        
        # 列出所有智能体
        agents = server.agent_manager.list_agents(actor=default_user)
        print(f"总共找到 {len(agents)} 个智能体")
        
        # 查找使用letta-free模型的智能体
        letta_free_agents = [agent for agent in agents if agent.llm_config.model == "letta-free"]
        print(f"找到 {len(letta_free_agents)} 个使用 letta-free 模型的智能体")
        
        # 修复这些智能体
        for agent in letta_free_agents:
            print(f"\n处理智能体: {agent.name} (ID: {agent.id})")
            print(f"  当前模型: {agent.llm_config.model}")
            print(f"  当前提供商: {agent.llm_config.provider_name}")
            
            # 更新智能体配置，使用Kimi模型
            try:
                # 创建UpdateAgent对象并设置model字段
                update_request = UpdateAgent(model="kimi/moonshot-v1-128k")
                
                updated_agent = server.update_agent(
                    agent_id=agent.id,
                    request=update_request,
                    actor=default_user
                )
                print(f"  ✅ 智能体已更新为使用 Kimi 模型")
                print(f"  新模型: {updated_agent.llm_config.model}")
                print(f"  新提供商: {updated_agent.llm_config.provider_name}")
            except Exception as e:
                print(f"  ❌ 更新智能体失败: {e}")
                
    except Exception as e:
        print(f"❌ 修复过程出错: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("Kimi智能体修复工具")
    print("=" * 50)
    
    # 修复现有智能体
    fix_kimi_agents()
    
    print("\n" + "=" * 50)
    print("🎉 修复完成！")
    print("建议重启Letta服务以确保所有配置正确加载。")


if __name__ == "__main__":
    main()