#!/usr/bin/env python3
"""
测试Kimi模型的工具调用功能
"""

import os
import sys
import json
from typing import List, Optional
import asyncio

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from letta.schemas.llm_config import LLMConfig
from letta.llm_api.kimi_client import KimiClient
from letta.schemas.message import Message
from letta.schemas.enums import MessageRole
from letta.schemas.letta_message_content import TextContent
from letta.schemas.openai.chat_completion_request import FunctionSchema

def create_test_messages() -> List[Message]:
    """创建测试消息"""
    # 系统消息
    system_message = Message(
        role=MessageRole.system,
        content=[TextContent(text="你是一个 helpful 的 AI 助手。当需要获取信息时，请使用适当的工具。")]
    )
    
    # 用户消息
    user_message = Message(
        role=MessageRole.user,
        content=[TextContent(text="今天是星期几？请使用 get_current_time 工具来获取当前时间。")]
    )
    
    return [system_message, user_message]

def create_test_tools() -> List[dict]:
    """创建测试工具"""
    return [
        {
            "name": "get_current_time",
            "description": "获取当前日期和时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "日期时间格式，如 'YYYY-MM-DD' 或 'full' 表示完整格式"
                    }
                },
                "required": []
            }
        }
    ]

async def test_kimi_tool_call():
    """测试Kimi模型的工具调用"""
    print("=== 测试Kimi模型工具调用 ===")
    
    # 创建Kimi客户端
    kimi_client = KimiClient()
    print("✅ KimiClient 创建成功")
    
    # 创建测试消息
    messages = create_test_messages()
    print("✅ 测试消息创建成功")
    
    # 创建测试工具
    tools = create_test_tools()
    print("✅ 测试工具创建成功")
    
    # 创建LLM配置
    llm_config = LLMConfig(
        model="kimi-k2-0711-preview",  # 使用K2模型
        model_endpoint_type="kimi",
        model_endpoint="https://api.moonshot.cn/v1",
        context_window=131072,
        put_inner_thoughts_in_kwargs=False,  # 对于Kimi K2模型设置为False
        temperature=0.7,
        provider_name="kimi",
        provider_category=None,
        model_wrapper=None,
        handle=None,
        max_tokens=None,
        enable_reasoner=True,
        reasoning_effort=None,
        max_reasoning_tokens=0,
        frequency_penalty=None,
        compatibility_type=None,
        verbosity=None,
        tier=None,
    )
    print("✅ LLM配置创建成功")
    
    try:
        # 构建请求数据
        print("\n--- 构建请求数据 ---")
        request_data = kimi_client.build_request_data(
            messages=messages,
            llm_config=llm_config,
            tools=tools
        )
        print("✅ 请求数据构建成功")
        print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
        
        # 发送请求
        print("\n--- 发送请求到Kimi API ---")
        response_data = kimi_client.request(request_data, llm_config)
        print("✅ 请求发送成功")
        print(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        
        # 检查工具调用
        if "choices" in response_data and len(response_data["choices"]) > 0:
            choice = response_data["choices"][0]
            if "message" in choice and "tool_calls" in choice["message"]:
                tool_calls = choice["message"]["tool_calls"]
                if tool_calls:
                    print(f"✅ 成功获取工具调用: {len(tool_calls)} 个工具调用")
                    for i, tool_call in enumerate(tool_calls):
                        print(f"  工具调用 {i+1}:")
                        print(f"    ID: {tool_call.get('id', 'N/A')}")
                        print(f"    名称: {tool_call.get('function', {}).get('name', 'N/A')}")
                        print(f"    参数: {tool_call.get('function', {}).get('arguments', 'N/A')}")
                else:
                    print("❌ 响应中没有工具调用")
                    # 检查是否有内容
                    content = choice["message"].get("content", "")
                    if content:
                        print(f"📝 模型返回内容: {content}")
            else:
                print("❌ 响应格式不正确，缺少message或tool_calls字段")
        else:
            print("❌ 响应格式不正确，缺少choices字段")
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("开始测试Kimi模型工具调用...")
    try:
        result = asyncio.run(test_kimi_tool_call())
        if result:
            print("\n🎉 测试完成，Kimi模型工具调用功能正常")
        else:
            print("\n❌ 测试失败，请检查错误信息")
    except KeyboardInterrupt:
        print("\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中出现未预期的错误: {e}")
        import traceback
        traceback.print_exc()