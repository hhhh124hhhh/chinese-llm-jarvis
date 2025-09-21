#!/usr/bin/env python3
"""
诊断401错误的脚本
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
import httpx
import json


def check_environment_variables():
    """检查环境变量"""
    print("=== 环境变量检查 ===")
    
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
    
    # 检查model_settings中的值
    print(f"\nModel settings:")
    print(f"  kimi_api_key: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"  kimi_base_url: {model_settings.kimi_base_url}")


def test_kimi_api_directly():
    """直接测试Kimi API"""
    print("\n=== 直接测试Kimi API ===")
    
    if not model_settings.kimi_api_key:
        print("❌ 未设置Kimi API密钥")
        return
        
    # 测试1: 获取模型列表
    print("1. 测试获取模型列表:")
    url = f"{model_settings.kimi_base_url}/models"
    headers = {
        "Authorization": f"Bearer {model_settings.kimi_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = httpx.get(url, headers=headers, timeout=10.0)
        print(f"   HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ API密钥验证成功")
            data = response.json()
            print(f"   可用模型数量: {len(data.get('data', []))}")
        elif response.status_code == 401:
            print("   ❌ API密钥验证失败 (401 Unauthorized)")
            print(f"   错误信息: {response.text}")
            return False
        else:
            print(f"   ❌ 请求失败 (状态码: {response.status_code})")
            print(f"   响应内容: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 请求出错: {e}")
        return False
    
    # 测试2: 简单聊天完成请求
    print("\n2. 测试聊天完成请求:")
    url = f"{model_settings.kimi_base_url}/chat/completions"
    payload = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "user", "content": "你好"}
        ],
        "max_tokens": 10
    }
    
    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=15.0)
        print(f"   HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ 聊天完成请求成功")
        elif response.status_code == 401:
            print("   ❌ 聊天完成请求失败 (401 Unauthorized)")
            print(f"   错误信息: {response.text}")
        else:
            print(f"   ❌ 聊天完成请求失败 (状态码: {response.status_code})")
            print(f"   响应内容: {response.text}")
            
    except Exception as e:
        print(f"   ❌ 聊天完成请求出错: {e}")
    
    return True


def check_letta_configuration():
    """检查Letta配置"""
    print("\n=== Letta配置检查 ===")
    
    try:
        server = SyncServer()
        print("✅ 服务器实例创建成功")
        
        # 检查启用的提供商
        provider_names = [provider.name for provider in server._enabled_providers]
        print(f"启用的提供商: {', '.join(provider_names)}")
        
        if "kimi" in provider_names:
            print("✅ Kimi提供商已启用")
        else:
            print("❌ Kimi提供商未启用")
            
        # 检查Kimi提供商配置
        kimi_providers = [p for p in server._enabled_providers if p.name == "kimi"]
        if kimi_providers:
            provider = kimi_providers[0]
            print(f"Kimi提供商API密钥: {'已设置' if provider.api_key else '未设置'}")
            print(f"Kimi提供商Base URL: {provider.base_url}")
            
    except Exception as e:
        print(f"❌ Letta配置检查失败: {e}")
        import traceback
        traceback.print_exc()


def check_api_key_format():
    """检查API密钥格式"""
    print("\n=== API密钥格式检查 ===")
    
    if model_settings.kimi_api_key:
        key = model_settings.kimi_api_key
        print(f"Kimi API密钥长度: {len(key)}")
        print(f"Kimi API密钥前缀: {key[:10] if len(key) > 10 else key}")
        
        # 检查是否为有效的sk-开头的密钥
        if key.startswith('sk-'):
            print("✅ Kimi API密钥格式正确")
        else:
            print("❌ Kimi API密钥格式可能不正确 (应以 'sk-' 开头)")
    else:
        print("❌ 未设置Kimi API密钥")


def main():
    """主函数"""
    print("401错误诊断工具")
    print("=" * 30)
    
    # 检查环境变量
    check_environment_variables()
    
    # 检查API密钥格式
    check_api_key_format()
    
    # 直接测试Kimi API
    test_kimi_api_directly()
    
    # 检查Letta配置
    check_letta_configuration()
    
    print("\n" + "=" * 30)
    print("诊断完成。如果问题仍然存在，请检查:")
    print("1. API密钥是否在Moonshot AI平台正确获取")
    print("2. API密钥是否有足够的权限")
    print("3. 网络连接是否正常")
    print("4. 是否有防火墙或代理阻止了请求")
    print("5. 重启服务以确保环境变量正确加载")


if __name__ == "__main__":
    main()