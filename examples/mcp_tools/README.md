# MCP工具使用示例

本目录包含了一些自定义MCP工具的示例，展示了如何扩展本地贾维斯系统的功能。

## 工具列表

### 1. 时间工具 (get_current_time.py)
提供获取当前时间和时间戳的功能。

### 2. 文件操作工具 (file_operations.py)
提供文件读写、列表和删除等操作。

## 使用方法

### 1. 配置MCP服务器
在Letta配置中添加MCP服务器：

```json
{
  "current_time": {
    "type": "stdio",
    "command": "python",
    "args": ["-m", "examples.mcp_tools.get_current_time"]
  },
  "file_operations": {
    "type": "stdio",
    "command": "python",
    "args": ["-m", "examples.mcp_tools.file_operations"]
  }
}
```

### 2. 在代理中使用工具
通过Letta客户端将工具添加到代理中：

```python
from letta_client import Letta

client = Letta(base_url="http://localhost:8283")

# 添加MCP服务器
client.tools.add_mcp_server({
    "server_name": "current_time",
    "type": "stdio",
    "command": "python",
    "args": ["-m", "examples.mcp_tools.get_current_time"]
})

# 获取工具列表
tools = client.tools.list_mcp_tools_by_server("current_time")

# 添加工具到代理
current_time_tool = client.tools.add_mcp_tool(
    mcp_server_name="current_time",
    mcp_tool_name="get_current_time"
)

# 将工具附加到代理
client.agents.tools.attach(
    agent_id="your_agent_id",
    tool_id=current_time_tool.id
)
```

## 开发自定义工具

### 1. 创建工具文件
创建一个新的Python文件，使用FastMCP框架：

```python
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("your_tool_name")

@mcp.tool()
def your_function(param1: str, param2: int = 10) -> str:
    """工具描述
    
    Args:
        param1: 参数1描述
        param2: 参数2描述，默认值为10
        
    Returns:
        返回值描述
    """
    # 实现工具逻辑
    return f"处理结果: {param1} - {param2}"

if __name__ == "__main__":
    # Run the server
    mcp.run(transport="stdio")
```

### 2. 注册工具
在MCP配置文件中添加新工具的配置。

### 3. 测试工具
使用Letta客户端测试工具功能。