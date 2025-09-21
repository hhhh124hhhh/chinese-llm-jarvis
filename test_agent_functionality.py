#!/usr/bin/env python3
"""
测试智能体功能的脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.settings import model_settings
from letta.server.server import SyncServer
from letta.schemas.message import MessageCreate
from letta.schemas.letta_message_content import TextContent
from letta.schemas.enums import MessageRole


def test_agent_messaging():
    """测试智能体消息功能"""
    print("=== 测试智能体消息功能 ===")
    
    try:
        # 创建服务器实例
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 获取默认用户
        from letta.services.user_manager import UserManager
        user_manager = UserManager()
        default_user = user_manager.get_default_user()
        print(f"✅ 获取默认用户: {default_user.id}")
        
        # 使用您提供的agent ID进行测试
        agent_id = "agent-de6786cd-a467-4dae-acd8-43fb20ec8955"
        
        # 创建测试消息
        test_message = MessageCreate(
            role=MessageRole.user,
            content=[TextContent(text="你好，请介绍一下你自己")],
        )
        
        print("正在发送测试消息...")
        
        # 发送消息给智能体
        usage_stats = server.send_messages(
            actor=default_user,
            agent_id=agent_id,
            input_messages=[test_message]
        )
        
        print("✅ 消息发送成功")
        print(f"使用统计: {usage_stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ 消息发送失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("智能体功能测试")
    print("=" * 30)
    
    success = test_agent_messaging()
    
    if success:
        print("\n🎉 智能体功能测试通过!")
    else:
        print("\n❌ 智能体功能测试失败")
        print("请检查以下可能的原因:")
        print("1. 确保智能体ID正确且智能体存在")
        print("2. 检查API密钥是否有效")
        print("3. 确保网络连接正常")
        print("4. 查看详细错误日志以获取更多信息")


if __name__ == "__main__":
    main()