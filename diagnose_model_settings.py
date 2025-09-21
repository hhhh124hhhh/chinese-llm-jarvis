#!/usr/bin/env python3
"""
诊断model_settings中的API密钥加载问题
"""

import os
from letta.settings import model_settings

def diagnose_model_settings():
    print("=== 诊断model_settings中的API密钥 ===")
    
    # 检查model_settings中的kimi_api_key
    print(f"model_settings.kimi_api_key: {repr(model_settings.kimi_api_key)}")
    
    # 检查环境变量
    env_kimi_api_key = os.environ.get('KIMI_API_KEY')
    print(f"os.environ.get('KIMI_API_KEY'): {repr(env_kimi_api_key)}")
    
    # 检查是否相等
    if model_settings.kimi_api_key == env_kimi_api_key:
        print("✅ model_settings和环境变量中的API密钥一致")
    else:
        print("❌ model_settings和环境变量中的API密钥不一致")
        print(f"  model_settings长度: {len(model_settings.kimi_api_key) if model_settings.kimi_api_key else 0}")
        print(f"  环境变量长度: {len(env_kimi_api_key) if env_kimi_api_key else 0}")
    
    # 检查model_settings是否正确加载了.env.local
    print("\n=== 检查ModelSettings配置 ===")
    print(f"ModelSettings类的env_file配置: {model_settings.model_config.get('env_file', '未设置')}")
    
    # 尝试重新加载设置
    print("\n=== 尝试重新加载设置 ===")
    try:
        # 重新实例化ModelSettings
        from letta.settings import ModelSettings
        new_model_settings = ModelSettings()
        print(f"新实例化的kimi_api_key: {repr(new_model_settings.kimi_api_key)}")
        
        if new_model_settings.kimi_api_key == model_settings.kimi_api_key:
            print("✅ 重新实例化后的API密钥一致")
        else:
            print("❌ 重新实例化后的API密钥不一致")
    except Exception as e:
        print(f"❌ 重新实例化时出错: {e}")

if __name__ == "__main__":
    diagnose_model_settings()