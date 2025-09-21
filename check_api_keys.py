#!/usr/bin/env python3
"""
检查API密钥配置的脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.settings import model_settings


def check_api_keys():
    """检查API密钥配置"""
    print("=== API密钥配置检查 ===")
    
    # 打印所有相关的环境变量
    print("相关环境变量:")
    for key, value in os.environ.items():
        if 'KIMI' in key or 'ZHIPU' in key or 'API_KEY' in key:
            # 隐藏API密钥的实际值
            if 'KEY' in key and value and len(value) > 10:
                print(f"  {key}: {'*' * (len(value)-8)}{value[-8:]}")
            else:
                print(f"  {key}: {value}")
    
    print("\nModel settings:")
    print(f"  kimi_api_key: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"  kimi_base_url: {model_settings.kimi_base_url}")
    print(f"  zhipu_api_key: {'已设置' if model_settings.zhipu_api_key else '未设置'}")
    print(f"  zhipu_base_url: {model_settings.zhipu_base_url}")
    
    # 验证Kimi API密钥格式
    if model_settings.kimi_api_key:
        print(f"\nKimi API密钥格式检查:")
        if model_settings.kimi_api_key.startswith('sk-'):
            print("  ✅ API密钥格式正确 (以 'sk-' 开头)")
        else:
            print("  ❌ API密钥格式可能不正确 (应以 'sk-' 开头)")
            print(f"     当前值: {model_settings.kimi_api_key}")
    
    return model_settings.kimi_api_key, model_settings.zhipu_api_key


def test_kimi_api_directly():
    """直接测试Kimi API"""
    import httpx
    import json
    
    print("\n=== 直接测试Kimi API ===")
    
    if not model_settings.kimi_api_key:
        print("❌ 未设置Kimi API密钥")
        return
        
    url = f"{model_settings.kimi_base_url}/models"
    headers = {
        "Authorization": f"Bearer {model_settings.kimi_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = httpx.get(url, headers=headers, timeout=10.0)
        print(f"HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Kimi API密钥验证成功")
            try:
                data = response.json()
                print(f"可用模型数量: {len(data.get('data', []))}")
                for model in data.get('data', [])[:3]:
                    print(f"  - {model.get('id', 'unknown')}")
            except:
                print("响应内容:", response.text[:200] + "..." if len(response.text) > 200 else response.text)
        elif response.status_code == 401:
            print("❌ Kimi API密钥验证失败 (401 Unauthorized)")
            print("错误信息:", response.text)
        else:
            print(f"❌ Kimi API请求失败 (状态码: {response.status_code})")
            print("响应内容:", response.text[:200] + "..." if len(response.text) > 200 else response.text)
            
    except Exception as e:
        print(f"❌ 测试Kimi API时出错: {e}")


def main():
    """主函数"""
    print("检查API密钥配置...")
    
    # 检查API密钥
    kimi_key, zhipu_key = check_api_keys()
    
    # 直接测试Kimi API
    test_kimi_api_directly()


if __name__ == "__main__":
    main()