@echo off
REM 本地贾维斯系统安装脚本
REM 适用于Windows

echo 🚀 开始安装本地贾维斯系统...

REM 检查是否已安装uv
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到uv，正在安装...
    powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"
    echo ✅ uv安装完成
) else (
    echo ✅ 已安装uv
)

REM 安装项目依赖
echo 📦 安装项目依赖...
uv sync --all-extras

REM 检查.env文件
if not exist .env (
    echo 📝 创建.env配置文件...
    if exist .env.example (
        copy .env.example .env
    ) else (
        echo # 本地贾维斯系统配置文件 > .env
    )
    echo 请编辑.env文件添加您的API密钥
)

echo ✅ 安装完成！
echo 使用以下命令启动服务：
echo uv run letta server

pause