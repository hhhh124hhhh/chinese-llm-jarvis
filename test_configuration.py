#!/usr/bin/env python3
"""
测试国产大模型配置
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from letta.settings import model_settings, settings
from letta.schemas.providers.kimi import KimiProvider
from letta.schemas.providers.zhipu import ZhipuProvider

def test_configuration():
    print("=== 测试国产大模型配置 ===")
    
    # 1. 检查环境变量
    print("\n1. 检查环境变量:")
    print(f"KIMI_API_KEY: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"ZHIPU_API_KEY: {'已设置' if model_settings.zhipu_api_key else '未设置'}")
    print(f"KIMI_BASE_URL: {model_settings.kimi_base_url}")
    print(f"ZHIPU_BASE_URL: {model_settings.zhipu_base_url}")
    
    # 2. 检查数据库配置
    print("\n2. 检查数据库配置:")
    print(f"存储类型: {settings.storage_type}")
    print(f"数据库引擎: {settings.database_engine}")
    print(f"SQLite路径: {settings.sqlite_db_path}")
    
    # 3. 测试Kimi Provider
    print("\n3. 测试Kimi Provider:")
    try:
        kimi_provider = KimiProvider()
        models = kimi_provider.list_llm_models()
        print(f"Kimi模型数量: {len(models)}")
        for model in models[:3]:  # 只显示前3个模型
            print(f"  - {model.handle}: {model.model} (上下文: {model.context_window})")
    except Exception as e:
        print(f"Kimi Provider错误: {e}")
    
    # 4. 测试Zhipu Provider
    print("\n4. 测试Zhipu Provider:")
    try:
        zhipu_provider = ZhipuProvider()
        models = zhipu_provider.list_llm_models()
        print(f"Zhipu模型数量: {len(models)}")
        for model in models[:3]:  # 只显示前3个模型
            print(f"  - {model.handle}: {model.model} (上下文: {model.context_window})")
    except Exception as e:
        print(f"Zhipu Provider错误: {e}")
    
    print("\n=== 配置测试完成 ===")

if __name__ == "__main__":
    test_configuration()