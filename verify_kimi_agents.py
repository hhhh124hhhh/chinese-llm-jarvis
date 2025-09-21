#!/usr/bin/env python3
"""
验证Kimi智能体配置的脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.server.server import SyncServer
from letta.services.user_manager import UserManager


def verify_kimi_agents():
    """验证智能体是否已正确更新为使用Kimi模型"""
    print("=== 验证Kimi智能体配置 ===")
    
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
        
        # 分类统计
        kimi_agents = []
        letta_free_agents = []
        other_agents = []
        
        for agent in agents:
            if agent.llm_config.provider_name == "kimi":
                kimi_agents.append(agent)
            elif agent.llm_config.model == "letta-free":
                letta_free_agents.append(agent)
            else:
                other_agents.append(agent)
        
        print(f"✅ Kimi模型智能体数量: {len(kimi_agents)}")
        print(f"⚠️  letta-free模型智能体数量: {len(letta_free_agents)}")
        print(f"ℹ️  其他模型智能体数量: {len(other_agents)}")
        
        # 详细显示每个智能体的信息
        print("\n=== 智能体详细信息 ===")
        for i, agent in enumerate(agents, 1):
            print(f"{i}. 智能体名称: {agent.name}")
            print(f"   ID: {agent.id}")
            print(f"   模型: {agent.llm_config.model}")
            print(f"   提供商: {agent.llm_config.provider_name}")
            print(f"   Base URL: {agent.llm_config.model_endpoint}")
            print()
            
        # 检查是否有仍然使用letta-free模型的智能体
        if letta_free_agents:
            print("⚠️  警告: 仍有智能体使用 letta-free 模型:")
            for agent in letta_free_agents:
                print(f"   - {agent.name} (ID: {agent.id})")
        else:
            print("✅ 所有智能体均已正确配置!")
            
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("Kimi智能体验证工具")
    print("=" * 50)
    
    # 验证环境变量
    print("=== 环境变量检查 ===")
    kimi_api_key = os.environ.get('KIMI_API_KEY')
    default_llm_handle = os.environ.get('LETTA_DEFAULT_LLM_HANDLE')
    
    if kimi_api_key:
        print(f"✅ KIMI_API_KEY 已设置 (长度: {len(kimi_api_key)})")
    else:
        print("❌ KIMI_API_KEY 未设置")
        
    if default_llm_handle:
        print(f"✅ LETTA_DEFAULT_LLM_HANDLE 已设置: {default_llm_handle}")
    else:
        print("❌ LETTA_DEFAULT_LLM_HANDLE 未设置")
    
    print()
    
    # 验证智能体配置
    verify_kimi_agents()
    
    print("=" * 50)
    print("验证完成！")


if __name__ == "__main__":
    main()