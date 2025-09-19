# 本地贾维斯系统 - Kimi和智谱AI模型使用指南

## 简介

本文档详细介绍如何在本地贾维斯系统中配置和使用Kimi（月之暗面）和智谱AI（GLM系列）模型。

## 配置API密钥

### 1. 获取API密钥

首先，您需要从相应的平台获取API密钥：

- **Kimi API密钥**：访问 [Moonshot AI平台](https://www.moonshot.cn/) 注册并获取API密钥
- **智谱AI API密钥**：访问 [智谱AI平台](https://open.bigmodel.cn/) 注册并获取API密钥

### 2. 配置环境变量

在 `.env` 文件中添加您的API密钥：

```bash
# Kimi (Moonshot AI)
KIMI_API_KEY=your_actual_kimi_api_key_here

# 智谱AI (Zhipu AI)
ZHIPU_API_KEY=your_actual_zhipu_api_key_here
```

## 可用模型列表

### Kimi模型

| 模型名称 | 上下文长度 | 特点 |
|---------|-----------|------|
| moonshot-v1-8k | 8K tokens | 基础版本，适合一般任务 |
| moonshot-v1-32k | 32K tokens | 中等长度上下文 |
| moonshot-v1-128k | 128K tokens | 长上下文版本 |
| kimi-k2-0905-preview | 256K tokens | Kimi K2系列预览版 |
| kimi-k2-0711-preview | 128K tokens | Kimi K2系列预览版 |
| kimi-k2-turbo-preview | 256K tokens | Kimi K2 Turbo版本 |

### 智谱AI模型

#### LLM模型

| 模型名称 | 上下文长度 | 特点 |
|---------|-----------|------|
| glm-4-plus | 128K tokens | GLM-4增强版 |
| glm-4-0520 | 128K tokens | GLM-4特定版本 |
| glm-4 | 128K tokens | 标准GLM-4 |
| glm-4-air | 128K tokens | 轻量级版本 |
| glm-4-airx | 128K tokens | 轻量级增强版 |
| glm-4-long | 1M tokens | 超长上下文版本 |
| glm-4-flash | 128K tokens | 快速响应版本 |
| glm-4-flashx | 128K tokens | 快速响应增强版 |
| glm-5 | 128K tokens | 最新GLM-5 |

#### 嵌入模型

| 模型名称 | 维度 | 特点 |
|---------|------|------|
| embedding-2 | 2048 | 第二代嵌入模型 |
| embedding-3 | 2048 | 第三代嵌入模型 |

## 使用示例

### 1. 创建使用Kimi模型的智能体

```python
from letta_client import Letta

# 连接到Letta服务器
client = Letta(base_url="http://localhost:8283")

# 使用Kimi模型创建智能体
kimi_agent = client.agents.create(
    name="kimi_assistant",
    model="kimi/moonshot-v1-128k",  # 使用128K上下文的Kimi模型
    embedding="letta/letta-free",
    memory_blocks=[
        {
            "label": "human",
            "value": "用户喜欢编程和AI技术"
        },
        {
            "label": "persona",
            "value": "我是你的AI助手，可以帮助你解答技术问题"
        }
    ],
    tools=["web_search", "get_current_time"]
)

# 与智能体对话
response = client.agents.messages.create(
    agent_id=kimi_agent.id,
    role="user",
    content="请帮我解释一下Transformer架构的工作原理"
)
```

### 2. 创建使用智谱AI模型的智能体

```python
from letta_client import Letta

# 连接到Letta服务器
client = Letta(base_url="http://localhost:8283")

# 使用智谱AI模型创建智能体
zhipu_agent = client.agents.create(
    name="zhipu_assistant",
    model="zhipu/glm-4-plus",  # 使用GLM-4增强版
    embedding="zhipu/embedding-3",  # 使用第三代嵌入模型
    memory_blocks=[
        {
            "label": "human",
            "value": "用户是AI研究者，对大模型技术有深入了解"
        },
        {
            "label": "persona",
            "value": "我是智谱AI助手，专注于大模型技术讨论"
        }
    ],
    tools=["web_search", "get_current_time"]
)

# 与智能体对话
response = client.agents.messages.create(
    agent_id=zhipu_agent.id,
    role="user",
    content="请分析一下当前大模型发展的趋势和挑战"
)
```

### 3. 模型切换示例

```python
# 创建多个使用不同模型的智能体
agents = {}

# Kimi智能体
agents["kimi"] = client.agents.create(
    name="kimi_writer",
    model="kimi/moonshot-v1-32k",
    tools=["web_search"]
)

# 智谱AI智能体
agents["zhipu"] = client.agents.create(
    name="zhipu_analyst",
    model="zhipu/glm-4-plus",
    tools=["web_search"]
)

# 根据任务选择合适的模型
def get_best_agent_for_task(task_type):
    if task_type == "creative_writing":
        return agents["kimi"]
    elif task_type == "technical_analysis":
        return agents["zhipu"]
    else:
        return agents["kimi"]  # 默认使用Kimi

# 使用选定的智能体处理任务
agent = get_best_agent_for_task("technical_analysis")
response = client.agents.messages.create(
    agent_id=agent.id,
    role="user",
    content="请分析当前AI芯片市场的发展趋势"
)
```

## 性能优化建议

### 1. 模型选择建议

- **创意写作、长文本生成**：推荐使用 Kimi 的长上下文模型（如 moonshot-v1-128k 或 kimi-k2 系列）
- **技术分析、代码理解**：推荐使用 智谱AI 的 GLM-4 系列模型
- **快速响应场景**：推荐使用 智谱AI 的 Flash 系列模型

### 2. 上下文管理

```python
# 合理设置上下文窗口
agent_config = {
    "kimi_long_context": {
        "model": "kimi/kimi-k2-0905-preview",
        "context_window": 262144  # 256K tokens
    },
    "zhipu_standard": {
        "model": "zhipu/glm-4-plus",
        "context_window": 131072  # 128K tokens
    }
}
```

### 3. 错误处理

```python
import time
from letta_client import Letta

def robust_model_call(client, agent_id, message, max_retries=3):
    """带重试机制的模型调用"""
    for attempt in range(max_retries):
        try:
            response = client.agents.messages.create(
                agent_id=agent_id,
                role="user",
                content=message
            )
            return response
        except Exception as e:
            print(f"第{attempt + 1}次尝试失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                raise e

# 使用示例
try:
    response = robust_model_call(client, agent_id, "请分析一下大模型的推理能力")
    print(response.messages[0].content)
except Exception as e:
    print(f"所有重试都失败了: {e}")
```

## 常见问题解答

### 1. API密钥配置后模型仍不可用

确保：
1. 已重启Letta服务以加载新的环境变量
2. API密钥格式正确且未过期
3. 网络连接正常

### 2. 模型响应速度慢

优化建议：
1. 选择适合任务的模型（不需要长上下文时使用标准模型）
2. 合理控制提示词长度
3. 使用缓存机制避免重复计算

### 3. 上下文长度超限

解决方案：
1. 使用支持更长上下文的模型
2. 实现上下文压缩或摘要机制
3. 分批处理长文档

## 进一步学习

- [Kimi官方文档](https://www.moonshot.cn/)
- [智谱AI官方文档](https://open.bigmodel.cn/)
- [Letta官方文档](https://letta.com/)