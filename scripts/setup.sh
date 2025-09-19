#!/bin/bash

# 本地贾维斯系统安装脚本
# 适用于Linux和macOS

echo "🚀 开始安装本地贾维斯系统..."

# 检查是否已安装uv
if ! command -v uv &> /dev/null
then
    echo "❌ 未找到uv，正在安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv安装完成"
else
    echo "✅ 已安装uv"
fi

# 安装项目依赖
echo "📦 安装项目依赖..."
uv sync --all-extras

# 检查.env文件
if [ ! -f .env ]; then
    echo "📝 创建.env配置文件..."
    cp .env.example .env 2>/dev/null || echo "# 本地贾维斯系统配置文件" > .env
    echo "请编辑.env文件添加您的API密钥"
fi

echo "✅ 安装完成！"
echo "使用以下命令启动服务："
echo "uv run letta server"