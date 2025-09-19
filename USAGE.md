# 本地贾维斯系统使用指南

## 快速开始

### 1. 安装和配置

#### 使用安装脚本 (推荐)
```bash
# Linux/macOS
./start.sh

# Windows
start.bat
```

#### 手动安装
```bash
# 1. 安装依赖
uv sync --all-extras

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加您的API密钥

# 3. 启动服务
uv run letta server
```

### 2. 配置国内大模型

在 `.env` 文件中添加您的API密钥：

```bash
# Kimi (Moonshot AI)
KIMI_API_KEY=your_kimi_api_key_here

# 智谱AI (Zhipu AI)
ZHIPU_API_KEY=your_zhipu_api_key_here

# 通义千问 (Qwen)
QWEN_API_KEY=your_qwen_api_key_here

# 文心一言 (ERNIE Bot)
ERNIE_API_KEY=your_ernie_api_key_here
```

### 3. 使用MCP工具

#### 使用内置MCP工具
```python
from letta_client import Letta

# 连接到Letta服务器
client = Letta(base_url="http://localhost:8283")

# 添加时间获取工具
client.tools.add_mcp_server({
    "server_name": "current_time",
    "type": "stdio",
    "command": "python",
    "args": ["-m", "examples.mcp_tools.get_current_time"]
})

# 获取工具并添加到代理
current_time_tool = client.tools.add_mcp_tool(
    mcp_server_name="current_time",
    mcp_tool_name="get_current_time"
)
```

#### 创建使用国内模型的代理
```python
# 使用Kimi模型创建代理
kimi_agent = client.agents.create(
    name="kimi_assistant",
    model="kimi/moonshot-v1-32k",
    embedding="openai/text-embedding-3-small",
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

# 使用智谱AI模型创建代理
zhipu_agent = client.agents.create(
    name="zhipu_assistant",
    model="zhipu/glm-4-plus",
    embedding="openai/text-embedding-3-small",
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
```

## 高级功能

### 1. 自定义MCP工具开发

创建一个简单的MCP工具：

```python
# my_tool.py
import datetime
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("my_tool")

@mcp.tool()
def get_system_info() -> str:
    """获取系统信息"""
    import platform
    return f"系统: {platform.system()} {platform.release()}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

注册工具：
```json
{
  "my_tool": {
    "type": "stdio",
    "command": "python",
    "args": ["my_tool.py"]
  }
}
```

### 2. 记忆管理

```python
# 创建具有长期记忆的代理
agent = client.agents.create(
    name="memory_agent",
    model="kimi/moonshot-v1-32k",
    memory_blocks=[
        {
            "label": "human",
            "value": "用户是AI开发者，喜欢研究大模型应用"
        },
        {
            "label": "persona",
            "value": "你是一个专业的AI助手，擅长技术问题解答"
        },
        {
            "label": "custom",
            "value": "用户的项目偏好：Python、FastAPI、PostgreSQL"
        }
    ]
)

# 与代理对话
response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[
        {
            "role": "user",
            "content": "我之前提到过什么项目偏好？"
        }
    ]
)
```

### 3. 多代理协作

```python
# 创建多个代理
researcher = client.agents.create(
    name="researcher",
    model="zhipu/glm-4-plus",
    memory_blocks=[
        {
            "label": "persona",
            "value": "你是一个研究助手，擅长信息收集和分析"
        }
    ]
)

writer = client.agents.create(
    name="writer",
    model="kimi/moonshot-v1-32k",
    memory_blocks=[
        {
            "label": "persona",
            "value": "你是一个写作助手，擅长撰写技术文档"
        }
    ]
)

# 让研究助手收集信息
research_response = client.agents.messages.create(
    agent_id=researcher.id,
    messages=[
        {
            "role": "user",
            "content": "请收集关于大模型推理优化的最新研究"
        }
    ]
)

# 将研究结果传递给写作助手
writer_response = client.agents.messages.create(
    agent_id=writer.id,
    messages=[
        {
            "role": "user",
            "content": f"基于以下研究结果，写一篇关于大模型推理优化的技术文章：{research_response.messages[-1].content}"
        }
    ]
)
```

## 故障排除

### 常见问题

1. **API密钥错误**
   - 检查 `.env` 文件中的API密钥是否正确
   - 确保环境变量已正确加载

2. **模型连接失败**
   - 检查网络连接
   - 验证API密钥和基础URL
   - 查看日志文件获取详细错误信息

3. **MCP工具无法加载**
   - 确保工具脚本具有执行权限
   - 检查工具配置是否正确
   - 验证Python环境和依赖包

### 查看日志
```bash
# 查看Letta服务器日志
tail -f logs/Letta.log

# 查看Docker容器日志
docker logs letta-jarvis
```

## API参考

### 代理管理
- `client.agents.create()` - 创建代理
- `client.agents.list()` - 列出代理
- `client.agents.get()` - 获取代理详情
- `client.agents.delete()` - 删除代理

### 消息交互
- `client.agents.messages.create()` - 发送消息
- `client.agents.messages.list()` - 列出消息历史

### 工具管理
- `client.tools.add_mcp_server()` - 添加MCP服务器
- `client.tools.list_mcp_tools_by_server()` - 列出MCP工具
- `client.tools.add_mcp_tool()` - 添加MCP工具到代理

### 模型管理
- `client.models.list_llms()` - 列出可用的LLM模型
- `client.models.list_embedding_models()` - 列出可用的嵌入模型

## 最佳实践

1. **模型选择**
   - 根据任务复杂度选择合适的模型
   - 考虑成本和性能平衡
   - 利用国内模型的本土化优势

2. **记忆管理**
   - 定期清理过时的记忆
   - 合理设置记忆块大小
   - 利用个性化记忆提升用户体验

3. **工具使用**
   - 为不同任务选择合适的工具
   - 定期更新和维护自定义工具
   - 监控工具执行性能和错误率

4. **安全性**
   - 妥善保管API密钥
   - 限制敏感操作的权限
   - 定期更新系统和依赖包