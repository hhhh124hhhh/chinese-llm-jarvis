import os
import sys
from letta.schemas.providers.kimi import KimiProvider
from letta.schemas.providers.zhipu import ZhipuProvider
from letta.schemas.enums import ProviderType, ProviderCategory

def test_kimi_provider():
    """测试Kimi提供商类"""
    print("=== 测试Kimi提供商 ===")
    
    # 创建Kimi提供商实例
    kimi_provider = KimiProvider(
        id=None,
        name="kimi",
        provider_type=ProviderType.kimi,
        provider_category=ProviderCategory.base,
        api_key=os.getenv("KIMI_API_KEY", "test_key"),
        base_url=None,
        access_key=None,
        region=None,
        api_version=None,
        organization_id=None,
        updated_at=None
    )
    
    # 测试模型列表
    llm_models = kimi_provider.list_llm_models()
    print(f"Kimi LLM模型数量: {len(llm_models)}")
    for model in llm_models:
        print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
    
    # 测试嵌入模型列表
    embedding_models = kimi_provider.list_embedding_models()
    print(f"Kimi嵌入模型数量: {len(embedding_models)}")
    
    print()

def test_zhipu_provider():
    """测试智谱AI提供商类"""
    print("=== 测试智谱AI提供商 ===")
    
    # 创建智谱AI提供商实例
    zhipu_provider = ZhipuProvider(
        id=None,
        name="zhipu",
        provider_type=ProviderType.zhipu,
        provider_category=ProviderCategory.base,
        api_key=os.getenv("ZHIPU_API_KEY", "test_key"),
        base_url=None,
        access_key=None,
        region=None,
        api_version=None,
        organization_id=None,
        updated_at=None
    )
    
    # 测试模型列表
    llm_models = zhipu_provider.list_llm_models()
    print(f"智谱AI LLM模型数量: {len(llm_models)}")
    for model in llm_models:
        print(f"  - {model.handle}: {model.model} (上下文窗口: {model.context_window})")
    
    # 测试嵌入模型列表
    embedding_models = zhipu_provider.list_embedding_models()
    print(f"智谱AI嵌入模型数量: {len(embedding_models)}")
    for model in embedding_models:
        print(f"  - {model.handle}: {model.embedding_model} (维度: {model.embedding_dim})")
    
    print()

def main():
    """主函数"""
    print("测试Kimi和智谱AI提供商类\n")
    
    try:
        test_kimi_provider()
        test_zhipu_provider()
        print("✅ 所有测试通过!")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()