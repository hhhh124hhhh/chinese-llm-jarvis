#!/usr/bin/env python3
"""
快速测试Kimi API的脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.settings import model_settings
import httpx


def quick_test():
    """快速测试Kimi API"""
    print("快速测试Kimi API")
    print("=" * 20)
    
    # 检查API密钥
    if not model_settings.kimi_api_key:
        print("❌ 未设置Kimi API密钥")
        return
        
    print(f"✅ API密钥已设置，长度: {len(model_settings.kimi_api_key)}")
    
    # 测试获取模型列表
    print("\n测试获取模型列表...")
    url = f"{model_settings.kimi_base_url}/models"
    headers = {
        "Authorization": f"Bearer {model_settings.kimi_api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = httpx.get(url, headers=headers, timeout=10.0)
        print(f"HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API密钥验证成功")
            data = response.json()
            print(f"可用模型数量: {len(data.get('data', []))}")
        elif response.status_code == 401:
            print("❌ API密钥验证失败 (401 Unauthorized)")
            print(f"错误信息: {response.text}")
        else:
            print(f"❌ 请求失败 (状态码: {response.status_code})")
            print(f"响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求出错: {e}")


if __name__ == "__main__":
    quick_test()