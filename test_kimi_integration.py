#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Kimi模型集成
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

def test_kimi_provider():
    """测试Kimi提供商配置"""
    print("=== 测试Kimi提供商 ===")
    try:
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 查找Kimi提供商
        kimi_provider = None
        for provider in server._enabled_providers:
            if provider.name == "kimi":
                kimi_provider = provider
                break
        
        if kimi_provider:
            print("✅ 找到Kimi提供商")
            print(f"  提供商名称: {kimi_provider.name}")
            print(f"  提供商类型: {kimi_provider.provider_type}")
            print(f"  API密钥: {'已设置' if kimi_provider.api_key else '未设置'}")
            if kimi_provider.api_key:
                print(f"    API密钥长度: {len(kimi_provider.api_key)}")
                print(f"    API密钥前缀: {kimi_provider.api_key[:8]}...")
            print(f"  Base URL: {kimi_provider.base_url}")
        else:
            print("❌ 未找到Kimi提供商")
            return False
            
    except Exception as e:
        print(f"❌ 服务器Kimi提供商测试失败: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_kimi_models():
    """测试Kimi模型列表"""
    print("\n=== 测试Kimi模型列表 ===")
    try:
        server = SyncServer()
        user_manager = UserManager()
        user = user_manager.get_default_user()
        
        # 通过服务器获取Kimi模型
        models = server.list_llm_models(actor=user, provider_name="kimi")
        print(f"✅ Kimi模型列表获取成功，共{len(models)}个模型")
        
        # 显示模型
        for i, model in enumerate(models[:5]):
            print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
            
        return True
    except Exception as e:
        print(f"❌ Kimi模型列表测试失败: {e}")
        traceback.print_exc()
        return False

def test_kimi_agent_creation():
    """测试使用Kimi模型创建智能体"""
    print("\n=== 测试使用Kimi模型创建智能体 ===")
    try:
        server = SyncServer()
        user_manager = UserManager()
        user = user_manager.get_default_user()
        print(f"✅ 获取默认用户: {user.id}")
        
        # 创建使用Kimi模型的智能体
        kimi_model_handle = "kimi/kimi-k2-0905-preview"
        
        # 检查模型是否存在
        try:
            llm_config = server.get_llm_config_from_handle(handle=kimi_model_handle, actor=user)
            print(f"✅ 找到Kimi模型: {llm_config.model}")
        except Exception as e:
            print(f"❌ 未找到Kimi模型 {kimi_model_handle}: {e}")
            # 列出所有可用的模型
            print("可用模型:")
            models = server.list_llm_models(actor=user)
            for model in models:
                if model.provider_name == "kimi":
                    print(f"  - {model.handle}")
            return False
        
        # 创建智能体
        agent_request = CreateAgent(
            name="kimi-test-agent",
            llm_config=llm_config,
            embedding_config=server.get_embedding_config_from_handle(handle="letta/letta-free", actor=user),
            include_base_tools=True,
        )
        
        agent = server.create_agent(request=agent_request, actor=user)
        print(f"✅ 智能体创建成功: {agent.name}")
        print(f"  ID: {agent.id}")
        print(f"  模型: {agent.llm_config.model}")
        print(f"  提供商: {agent.llm_config.provider_name}")
        print(f"  Base URL: {agent.llm_config.model_endpoint}")
        
        # 测试发送消息
        message = MessageCreate(
            role=MessageRole.user,
            content=[TextContent(text="你好，我是测试用户")],
        )
        
        # 发送消息到智能体
        usage = server.send_messages(
            actor=user,
            agent_id=agent.id,
            input_messages=[message],
        )
        print("✅ 消息发送成功")
        
        # 清理：删除测试智能体
        server.agent_manager.delete_agent(agent_id=agent.id, actor=user)
        print("✅ 测试智能体已清理")
        
        return True
    except Exception as e:
        print(f"❌ Kimi智能体创建测试失败: {e}")
        traceback.print_exc()
        return False

def test_direct_kimi_request():
    """直接测试Kimi API请求"""
    print("\n=== 直接测试Kimi API请求 ===")
    try:
        # 创建KimiClient
        kimi_client = KimiClient()
        print("✅ KimiClient实例创建成功")
        
        # 创建LLM配置
        llm_config = LLMConfig(
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
        client_kwargs = kimi_client._prepare_client_kwargs(llm_config)
        print("✅ 客户端参数准备成功")
        print(f"  API密钥: {'已设置' if client_kwargs.get('api_key') else '未设置'}")
        print(f"  Base URL: {client_kwargs.get('base_url')}")
        
        # 构建请求数据
        from letta.schemas.message import Message
        messages = [
            Message(role=MessageRole.user, content=[TextContent(text="你好，请简单介绍一下你自己")])
        ]
        
        request_data = kimi_client.build_request_data(
            messages=messages,
            llm_config=llm_config
        )
        print("✅ 请求数据构建成功")
        print(f"  模型: {request_data.get('model')}")
        print(f"  消息数量: {len(request_data.get('messages', []))}")
        
        # 发送请求
        response = kimi_client.request(request_data=request_data, llm_config=llm_config)
        print("✅ API请求成功")
        print(f"  响应类型: {response.get('object')}")
        print(f"  选择数量: {len(response.get('choices', []))}")
        
        # 显示第一个选择的内容
        if response.get('choices'):
            first_choice = response['choices'][0]
            if 'message' in first_choice and 'content' in first_choice['message']:
                content = first_choice['message']['content']
                print(f"  响应内容: {content[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ 直接Kimi API请求测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    print("Kimi模型集成测试")
    print("=" * 30)
    
    # 检查基本配置
    print("=== 基本配置检查 ===")
    print(f"Kimi API密钥: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"Kimi Base URL: {model_settings.kimi_base_url}")
    
    # 运行各项测试
    tests = [
        ("Kimi提供商", test_kimi_provider),
        ("Kimi模型列表", test_kimi_models),
        ("直接Kimi API请求", test_direct_kimi_request),
        ("Kimi智能体创建", test_kimi_agent_creation),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n运行测试: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试 {test_name} 异常: {e}")
            traceback.print_exc()
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 30)
    print("测试结果汇总:")
    all_passed = True
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有测试通过！Kimi模型集成正常。")
    else:
        print("\n❌ 部分测试失败，请检查以上错误信息。")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)