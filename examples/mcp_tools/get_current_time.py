import datetime
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("current_time")


@mcp.tool()
def get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前系统时间
    
    Args:
        format: 时间格式，默认为 "%Y-%m-%d %H:%M:%S"
        
    Returns:
        格式化后的当前时间字符串
    """
    return datetime.datetime.now().strftime(format)


@mcp.tool()
def get_timestamp() -> int:
    """获取当前时间戳
    
    Returns:
        当前时间戳（秒）
    """
    return int(datetime.datetime.now().timestamp())


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")