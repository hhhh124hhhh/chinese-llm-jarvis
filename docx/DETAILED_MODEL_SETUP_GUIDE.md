# 本地贾维斯系统 - 详细模型设置指南

## 目录
1. [概述](#概述)
2. [环境变量配置](#环境变量配置)
3. [支持的模型提供商](#支持的模型提供商)
4. [Kimi模型配置](#kimi模型配置)
5. [智谱AI模型配置](#智谱ai模型配置)
6. [其他模型配置](#其他模型配置)
7. [模型使用方法](#模型使用方法)
8. [故障排除](#故障排除)
9. [最佳实践](#最佳实践)

## 概述

本地贾维斯系统基于Letta平台构建，支持多种国内外大语言模型。本指南将详细介绍如何配置和使用各种模型，包括国内的Kimi（月之暗面）和智谱AI（GLM系列）模型。

## 环境变量配置

### 1. 配置文件位置

系统支持以下配置文件：
- `.env` - 主配置文件
- `.env.local` - 本地配置文件（优先级更高）

### 2. 基本配置结构

```bash
# 数据库配置
LETTA_PG_DB=letta
LETTA_PG_USER=letta
LETTA_PG_PASSWORD=letta
LETTA_PG_HOST=localhost
LETTA_PG_PORT=5432

# 国内大模型API密钥
KIMI_API_KEY=your_kimi_api_key_here
ZHIPU_API_KEY=your_zhipu_api_key_here
QWEN_API_KEY=your_qwen_api_key_here
ERNIE_API_KEY=your_ernie_api_key_here

# 其他模型API密钥
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# 本地模型配置
OLLAMA_BASE_URL=http://localhost:11434
LMSTUDIO_BASE_URL=http://localhost:1234/v1

# MCP工具配置
COMPOSIO_API_KEY=your_composio_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
EXA_API_KEY=your_exa_api_key_here

# 其他配置
LETTA_DEBUG=True
```

### 3. 配置文件优先级

系统按照以下优先级加载配置：
1. 环境变量
2. `.env.local`
3. `.env`

## 支持的模型提供商

### 1. 国内模型提供商

| 提供商 | 环境变量 | 默认Base URL | 状态 |
|-------|---------|-------------|------|
| Kimi (Moonshot AI) | KIMI_API_KEY | https://api.moonshot.cn/v1 | ✅ 支持 |
| 智谱AI (Zhipu AI) | ZHIPU_API_KEY | https://open.bigmodel.cn/api/paas/v4 | ✅ 支持 |
| 通义千问 (Qwen) | QWEN_API_KEY | - | 计划支持 |
| 文心一言 (ERNIE Bot) | ERNIE_API_KEY | - | 计划支持 |

### 2. 国外模型提供商

| 提供商 | 环境变量 | 默认Base URL | 状态 |
|-------|---------|-------------|------|
| OpenAI | OPENAI_API_KEY | https://api.openai.com/v1 | ✅ 支持 |
| Anthropic | ANTHROPIC_API_KEY | - | ✅ 支持 |
| Google Gemini | GEMINI_API_KEY | https://generativelanguage.googleapis.com/ | ✅ 支持 |
| Groq | GROQ_API_KEY | - | ✅ 支持 |

## Kimi模型配置

### 1. 获取API密钥

1. 访问 [Moonshot AI平台](https://www.moonshot.cn/)
2. 注册账号并登录
3. 进入API密钥管理页面
4. 创建新的API密钥
5. 复制API密钥

### 2. 配置API密钥

在 `.env` 或 `.env.local` 文件中添加：

```bash
KIMI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. 可用Kimi模型

| 模型名称 | 上下文长度 | 特点 | 推荐用途 |
|---------|-----------|------|---------|
| moonshot-v1-8k | 8K tokens | 基础版本 | 一般任务 |
| moonshot-v1-32k | 32K tokens | 中等长度上下文 | 文档处理 |
| moonshot-v1-128k | 128K tokens | 长上下文版本 | 长文档分析 |
| kimi-k2-0905-preview | 256K tokens | Kimi K2系列预览版 | 超长上下文 |
| kimi-k2-0711-preview | 128K tokens | Kimi K2系列预览版 | 长上下文任务 |
| kimi-k2-turbo-preview | 256K tokens | Kimi K2 Turbo版本 | 快速长上下文 |

### 4. 模型调用格式

在创建智能体时使用以下格式：

```python
# 使用Kimi模型创建智能体
agent = client.agents.create(
    name="kimi_assistant",
    model="kimi/moonshot-v1-128k",  # 格式: provider/model_name
    embedding="letta/letta-free"
)
```

## 智谱AI模型配置

### 1. 获取API密钥

1. 访问 [智谱AI平台](https://open.bigmodel.cn/)
2. 注册账号并登录
3. 进入API密钥管理页面
4. 创建新的API密钥
5. 复制API密钥

### 2. 配置API密钥

在 `.env` 或 `.env.local` 文件中添加：

```bash
ZHIPU_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx
```

### 3. 可用智谱AI模型

#### LLM模型

| 模型名称 | 上下文长度 | 特点 | 推荐用途 |
|---------|-----------|------|---------|
| glm-4-plus | 128K tokens | GLM-4增强版 | 复杂任务 |
| glm-4-0520 | 128K tokens | GLM-4特定版本 | 技术分析 |
| glm-4 | 128K tokens | 标准GLM-4 | 通用任务 |
| glm-4-air | 128K tokens | 轻量级版本 | 快速响应 |
| glm-4-airx | 128K tokens | 轻量级增强版 | 快速复杂任务 |
| glm-4-long | 1M tokens | 超长上下文版本 | 超长文档 |
| glm-4-flash | 128K tokens | 快速响应版本 | 简单任务 |
| glm-4-flashx | 128K tokens | 快速响应增强版 | 快速复杂任务 |
| glm-5 | 128K tokens | 最新GLM-5 | 最新功能 |

#### 嵌入模型

| 模型名称 | 维度 | 特点 |
|---------|------|------|
| embedding-2 | 2048 | 第二代嵌入模型 |
| embedding-3 | 2048 | 第三代嵌入模型 |

### 4. 模型调用格式

在创建智能体时使用以下格式：

```python
# 使用智谱AI模型创建智能体
agent = client.agents.create(
    name="zhipu_assistant",
    model="zhipu/glm-4-plus",  # 格式: provider/model_name
    embedding="zhipu/embedding-3"  # 使用智谱AI嵌入模型
)
```

## 其他模型配置

### 1. OpenAI模型

配置API密钥：

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. 本地模型 (Ollama)

配置Base URL：

```bash
OLLAMA_BASE_URL=http://localhost:11434
```

### 3. 本地模型 (LMStudio)

配置Base URL：

```bash
LMSTUDIO_BASE_URL=http://localhost:1234/v1
```

## 模型使用方法

### 1. 通过Letta客户端使用

```python
from letta_client import Letta

# 连接到Letta服务器
client = Letta(base_url="http://localhost:8283")

# 创建使用Kimi模型的智能体
kimi_agent = client.agents.create(
    name="kimi_assistant",
    model="kimi/moonshot-v1-128k",
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
    ]
)

# 与智能体对话
response = client.agents.messages.create(
    agent_id=kimi_agent.id,
    role="user",
    content="请帮我解释一下Transformer架构的工作原理"
)
```

### 2. 通过API直接调用

```python
import requests

# 获取可用模型列表
response = requests.get("http://localhost:8283/v1/models")
models = response.json()
print(models)

# 创建智能体
agent_data = {
    "name": "my_agent",
    "model": "kimi/moonshot-v1-128k",
    "embedding": "letta/letta-free"
}

response = requests.post("http://localhost:8283/v1/agents", json=agent_data)
agent = response.json()
```

### 3. 模型切换示例

```python
# 创建多个使用不同模型的智能体
agents = {}

# Kimi智能体
agents["kimi"] = client.agents.create(
    name="kimi_writer",
    model="kimi/moonshot-v1-32k"
)

# 智谱AI智能体
agents["zhipu"] = client.agents.create(
    name="zhipu_analyst",
    model="zhipu/glm-4-plus"
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

## 故障排除

### 1. 401认证错误

**问题**: `Error code: 401 - {'error': {'message': 'Invalid Authentication', 'type': 'invalid_authentication_error'}}`

**解决方案**:
1. 检查API密钥是否正确配置
2. 验证API密钥格式是否正确（Kimi应以`sk-`开头）
3. 确认API密钥未过期
4. 重启服务以重新加载环境变量

```bash
# 检查环境变量
echo $KIMI_API_KEY

# 重启服务
./start.sh
```

### 2. 模型不可用

**问题**: 模型在前端不显示或无法选择

**解决方案**:
1. 检查API密钥是否已正确配置
2. 确认提供商未被禁用（检查`LETTA_DISABLE_*_PROVIDER`环境变量）
3. 验证网络连接是否正常
4. 查看服务日志确认提供商是否成功加载

### 3. 网络连接问题

**问题**: 请求超时或连接失败

**解决方案**:
1. 检查网络连接
2. 配置代理（如果需要）
3. 调整超时设置
4. 使用国内镜像站点（如果可用）

### 4. 诊断脚本

使用诊断脚本检查配置：

```bash
# 运行诊断脚本
python diagnose_401_error.py
```

## 最佳实践

### 1. 模型选择建议

- **创意写作、长文本生成**: 推荐使用 Kimi 的长上下文模型
- **技术分析、代码理解**: 推荐使用 智谱AI 的 GLM-4 系列模型
- **快速响应场景**: 推荐使用 智谱AI 的 Flash 系列模型
- **超长文档处理**: 推荐使用 Kimi K2 系列或智谱AI的long模型

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
```

### 4. 性能优化

1. **选择合适的模型**: 根据任务复杂度选择适当的模型
2. **控制提示词长度**: 避免过长的提示词影响性能
3. **使用缓存机制**: 对重复请求使用缓存
4. **合理设置超时**: 根据模型响应时间调整超时设置

## 附录

### 1. 常用命令

```bash
# 启动服务
./start.sh

# 检查服务状态
ps aux | grep letta

# 查看日志
tail -f ~/.letta/logs/Letta.log

# 重启服务
pkill -f letta && ./start.sh
```

### 2. 环境变量参考

| 环境变量 | 说明 | 默认值 |
|---------|------|-------|
| KIMI_API_KEY | Kimi API密钥 | None |
| ZHIPU_API_KEY | 智谱AI API密钥 | None |
| LETTA_DISABLE_KIMI_PROVIDER | 禁用Kimi提供商 | False |
| LETTA_DISABLE_ZHIPU_PROVIDER | 禁用智谱AI提供商 | False |
| LETTA_DEBUG | 启用调试模式 | False |
| LETTA_PG_DB | PostgreSQL数据库名 | letta |
| LETTA_PG_USER | PostgreSQL用户名 | letta |
| LETTA_PG_PASSWORD | PostgreSQL密码 | letta |
| LETTA_PG_HOST | PostgreSQL主机 | localhost |
| LETTA_PG_PORT | PostgreSQL端口 | 5432 |

### 3. 支持资源

- [Kimi官方文档](https://www.moonshot.cn/)
- [智谱AI官方文档](https://open.bigmodel.cn/)
- [Letta官方文档](https://letta.com/)
- [项目GitHub仓库](https://github.com/your-repo/chinese-llm-jarvis)