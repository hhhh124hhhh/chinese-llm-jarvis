#!/usr/bin/env python3
"""
快速检查脚本
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from letta.settings import model_settings


def quick_check():
    """快速检查"""
    print("快速检查")
    print("=" * 10)
    
    # 检查环境变量
    kimi_api_key = os.environ.get('KIMI_API_KEY', '未设置')
    print(f"环境变量 KIMI_API_KEY: {'已设置' if kimi_api_key != '未设置' else '未设置'}")
    
    # 检查model_settings
    print(f"model_settings.kimi_api_key: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    
    if model_settings.kimi_api_key:
        print(f"API密钥长度: {len(model_settings.kimi_api_key)}")
        print(f"API密钥前缀: {model_settings.kimi_api_key[:10]}")
    
    print(f"Base URL: {model_settings.kimi_base_url}")


if __name__ == "__main__":
    quick_check()