#!/usr/bin/env python3
"""
诊断和修复脚本：解决AI API加载问题
"""
import os
import sys
import json
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from letta.settings import model_settings, settings
from letta.schemas.providers.kimi import KimiProvider
from letta.schemas.providers.zhipu import ZhipuProvider
from letta.schemas.enums import ProviderType, ProviderCategory

def check_env_file():
    """检查.env.local文件"""
    env_file = Path("d:/chinese-llm-jarvis/.env.local")
    if not env_file.exists():
        print("❌ .env.local文件不存在")
        return False
    
    print("✅ .env.local文件存在")
    return True

def load_environment_variables():
    """从.env.local文件加载环境变量"""
    env_file = Path("d:/chinese-llm-jarvis/.env.local")
    if not env_file.exists():
        return False
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if value:
                            os.environ[key] = value
        return True
    except Exception as e:
        print(f"❌ 加载环境变量时出错: {e}")
        return False

def diagnose_api_keys():
    """诊断API密钥配置"""
    print("\n=== API密钥诊断 ===")
    
    # 检查环境变量中的API密钥
    kimi_api_key = os.getenv("KIMI_API_KEY")
    zhipu_api_key = os.getenv("ZHIPU_API_KEY")
    
    print(f"环境变量 KIMI_API_KEY: {'已设置' if kimi_api_key else '未设置'}")
    print(f"环境变量 ZHIPU_API_KEY: {'已设置' if zhipu_api_key else '未设置'}")
    
    # 检查model_settings中的API密钥
    print(f"model_settings.kimi_api_key: {'已设置' if model_settings.kimi_api_key else '未设置'}")
    print(f"model_settings.zhipu_api_key: {'已设置' if model_settings.zhipu_api_key else '未设置'}")
    
    # 检查Base URLs
    print(f"Kimi Base URL: {model_settings.kimi_base_url}")
    print(f"智谱AI Base URL: {model_settings.zhipu_base_url}")
    
    return kimi_api_key, zhipu_api_key

def test_kimi_provider(api_key):
    """测试Kimi提供商"""
    print("\n=== 测试Kimi提供商 ===")
    
    if not api_key:
        print("❌ 跳过Kimi测试 - 未设置API密钥")
        return False
    
    try:
        kimi_provider = KimiProvider(
            id=None,
            name="kimi",
            provider_type=ProviderType.kimi,
            provider_category=ProviderCategory.base,
            api_key=api_key,
            base_url=model_settings.kimi_base_url,
            access_key=None,
            region=None,
            api_version=None,
            organization_id=None,
            updated_at=None
        )
        
        print("✅ Kimi提供商实例创建成功")
        
        # 测试模型列表
        llm_models = kimi_provider.list_llm_models()
        print(f"✅ Kimi LLM模型数量: {len(llm_models)}")
        
        if llm_models:
            print("前3个模型:")
            for model in llm_models[:3]:
                print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
        
        return True
        
    except Exception as e:
        print(f"❌ Kimi提供商测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_zhipu_provider(api_key):
    """测试智谱AI提供商"""
    print("\n=== 测试智谱AI提供商 ===")
    
    if not api_key:
        print("❌ 跳过智谱AI测试 - 未设置API密钥")
        return False
    
    try:
        zhipu_provider = ZhipuProvider(
            id=None,
            name="zhipu",
            provider_type=ProviderType.zhipu,
            provider_category=ProviderCategory.base,
            api_key=api_key,
            base_url=model_settings.zhipu_base_url,
            access_key=None,
            region=None,
            api_version=None,
            organization_id=None,
            updated_at=None
        )
        
        print("✅ 智谱AI提供商实例创建成功")
        
        # 测试模型列表
        llm_models = zhipu_provider.list_llm_models()
        print(f"✅ 智谱AI LLM模型数量: {len(llm_models)}")
        
        if llm_models:
            print("前3个模型:")
            for model in llm_models[:3]:
                print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
        
        # 测试嵌入模型
        embedding_models = zhipu_provider.list_embedding_models()
        print(f"✅ 智谱AI嵌入模型数量: {len(embedding_models)}")
        
        if embedding_models:
            print("嵌入模型:")
            for model in embedding_models:
                print(f"  - {model.handle}: {model.embedding_model} (维度: {model.embedding_dim})")
        
        return True
        
    except Exception as e:
        print(f"❌ 智谱AI提供商测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_server_initialization():
    """检查服务器初始化过程中的提供商加载"""
    print("\n=== 检查服务器提供商加载 ===")
    
    try:
        from letta.server.server import SyncServer
        
        # 创建服务器实例
        server = SyncServer()
        
        # 检查已启用的提供商
        enabled_providers = server._enabled_providers
        print(f"✅ 已启用的提供商数量: {len(enabled_providers)}")
        
        provider_names = [provider.name for provider in enabled_providers]
        print(f"已启用的提供商: {', '.join(provider_names)}")
        
        # 检查是否有Kimi或智谱AI提供商
        kimi_enabled = any(provider.name == "kimi" for provider in enabled_providers)
        zhipu_enabled = any(provider.name == "zhipu" for provider in enabled_providers)
        
        print(f"Kimi提供商已启用: {'是' if kimi_enabled else '否'}")
        print(f"智谱AI提供商已启用: {'是' if zhipu_enabled else '否'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 服务器初始化检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def provide_fix_suggestions():
    """提供修复建议"""
    print("\n=== 修复建议 ===")
    print("1. 确保在.env.local文件中设置了实际的API密钥:")
    print("   - KIMI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print("   - ZHIPU_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print()
    print("2. 获取API密钥:")
    print("   - Kimi API密钥: 访问 https://www.moonshot.cn/")
    print("   - 智谱AI API密钥: 访问 https://open.bigmodel.cn/")
    print()
    print("3. 重启服务以应用更改:")
    print("   - 使用 start_windows.bat 或 start_server.py 启动服务")
    print()
    print("4. 验证配置:")
    print("   - 运行此脚本再次检查配置是否正确")

def main():
    """主函数"""
    print("AI API加载问题诊断和修复工具")
    print("=" * 40)
    
    # 检查环境文件
    if not check_env_file():
        print("\n请创建.env.local文件并配置API密钥")
        provide_fix_suggestions()
        return False
    
    # 加载环境变量
    print("\n加载环境变量...")
    if not load_environment_variables():
        print("❌ 无法加载环境变量")
        return False
    
    # 诊断API密钥
    kimi_key, zhipu_key = diagnose_api_keys()
    
    # 测试提供商
    kimi_test = test_kimi_provider(kimi_key)
    zhipu_test = test_zhipu_provider(zhipu_key)
    
    # 检查服务器初始化
    server_check = check_server_initialization()
    
    # 总结
    print("\n=== 诊断结果 ===")
    if kimi_test and zhipu_test and server_check:
        print("✅ 所有检查通过! API加载正常")
        return True
    else:
        print("❌ 存在问题需要修复")
        provide_fix_suggestions()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)