#!/usr/bin/env python3
"""
测试修复后的Kimi API密钥
"""

import os
import httpx
from letta.settings import model_settings

def test_api_key():
    print("=== 测试修复后的Kimi API密钥 ===")
    
    # 检查环境变量
    env_api_key = os.getenv('KIMI_API_KEY')
    print(f"环境变量中的API密钥: {repr(env_api_key)}")
    
    # 检查model_settings
    settings_api_key = model_settings.kimi_api_key
    print(f"Model settings中的API密钥: {repr(settings_api_key)}")
    
    # 直接从文件读取
    env_file_path = os.path.join(os.path.dirname(__file__), '.env.local')
    with open(env_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for line in content.split('\n'):
        if line.startswith('KIMI_API_KEY='):
            file_api_key = line.split('=', 1)[1]
            print(f"文件中的API密钥: {repr(file_api_key)}")
            break
    
    # 测试API调用
    if settings_api_key:
        print("\n=== 测试Kimi API调用 ===")
        url = "https://api.moonshot.cn/v1/models"
        headers = {
            "Authorization": f"Bearer {settings_api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = httpx.get(url, headers=headers, timeout=30.0)
            print(f"API请求状态码: {response.status_code}")
            if response.status_code == 200:
                print("✅ API密钥认证成功!")
                data = response.json()
                print(f"可用模型数量: {len(data.get('data', []))}")
            else:
                print(f"❌ API请求失败: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ API请求异常: {e}")
    else:
        print("❌ 未找到API密钥")

if __name__ == "__main__":
    test_api_key()