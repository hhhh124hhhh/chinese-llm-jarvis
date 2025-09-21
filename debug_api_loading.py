#!/usr/bin/env python3
"""
Debug script to check AI API loading issues
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from letta.settings import model_settings, settings
from letta.schemas.providers.kimi import KimiProvider
from letta.schemas.providers.zhipu import ZhipuProvider
from letta.schemas.enums import ProviderType, ProviderCategory

def check_environment_variables():
    """Check if required environment variables are set"""
    print("=== 环境变量检查 ===")
    
    # Check for API keys
    kimi_api_key = os.getenv("KIMI_API_KEY")
    zhipu_api_key = os.getenv("ZHIPU_API_KEY")
    
    print(f"KIMI_API_KEY: {'已设置' if kimi_api_key else '未设置'}")
    print(f"ZHIPU_API_KEY: {'已设置' if zhipu_api_key else '未设置'}")
    
    # Check for base URLs
    kimi_base_url = os.getenv("KIMI_BASE_URL", model_settings.kimi_base_url)
    zhipu_base_url = os.getenv("ZHIPU_BASE_URL", model_settings.zhipu_base_url)
    
    print(f"KIMI_BASE_URL: {kimi_base_url}")
    print(f"ZHIPU_BASE_URL: {zhipu_base_url}")
    
    return kimi_api_key, zhipu_api_key

def test_kimi_provider(api_key):
    """Test Kimi provider loading"""
    print("\n=== 测试Kimi提供商 ===")
    
    if not api_key:
        print("跳过Kimi测试 - 未设置API密钥")
        return
    
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
        
        print("Kimi提供商实例创建成功")
        
        # Test model listing
        llm_models = kimi_provider.list_llm_models()
        print(f"Kimi LLM模型数量: {len(llm_models)}")
        for model in llm_models[:3]:  # Show first 3 models
            print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
            
        print("✅ Kimi提供商测试通过")
        return True
        
    except Exception as e:
        print(f"❌ Kimi提供商测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_zhipu_provider(api_key):
    """Test Zhipu provider loading"""
    print("\n=== 测试智谱AI提供商 ===")
    
    if not api_key:
        print("跳过智谱AI测试 - 未设置API密钥")
        return
    
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
        
        print("智谱AI提供商实例创建成功")
        
        # Test model listing
        llm_models = zhipu_provider.list_llm_models()
        print(f"智谱AI LLM模型数量: {len(llm_models)}")
        for model in llm_models[:3]:  # Show first 3 models
            print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
            
        # Test embedding models
        embedding_models = zhipu_provider.list_embedding_models()
        print(f"智谱AI嵌入模型数量: {len(embedding_models)}")
        for model in embedding_models:
            print(f"  - {model.handle}: {model.embedding_model} (维度: {model.embedding_dim})")
            
        print("✅ 智谱AI提供商测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 智谱AI提供商测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("调试AI API加载问题\n")
    
    # Check environment variables
    kimi_api_key, zhipu_api_key = check_environment_variables()
    
    # Test providers
    kimi_success = test_kimi_provider(kimi_api_key)
    zhipu_success = test_zhipu_provider(zhipu_api_key)
    
    print("\n=== 总结 ===")
    if kimi_success and zhipu_success:
        print("✅ 所有提供商测试通过!")
    elif kimi_success or zhipu_success:
        print("⚠️ 部分提供商测试通过")
    else:
        print("❌ 所有提供商测试失败")
        
    print("\n提示:")
    print("1. 确保在.env文件中设置了正确的API密钥")
    print("2. 确保API密钥有效且未过期")
    print("3. 检查网络连接是否正常")
    print("4. 重启服务以加载新的环境变量")

if __name__ == "__main__":
    main()