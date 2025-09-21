@echo off
echo 启动Letta服务器 (Windows版本)

:: 设置Windows环境变量
set TEMP=%SystemRoot%\TEMP
set TMP=%SystemRoot%\TEMP

:: 检查依赖
echo 检查Python安装...
python --version
if %errorlevel% neq 0 (
    echo 错误: Python未安装或未在PATH中
    pause
    exit /b 1
)

echo 检查uv安装...
uv --version
if %errorlevel% neq 0 (
    echo 错误: uv未安装或未在PATH中
    pause
    exit /b 1
)

:: 加载环境变量 (如果存在)
if exist ".env.local" (
    echo 加载环境变量从 .env.local
    for /f "tokens=1,2 delims==" %%a in (.env.local) do (
        set %%a=%%b
    )
)

:: 构建启动命令
set "cmd=uv run letta server"

:: 添加参数
:parse_args
if "%~1"=="" goto start_server
if "%~1"=="--debug" (
    set "cmd=%cmd% --debug"
    shift
    goto parse_args
)
if "%~1"=="--port" (
    set "cmd=%cmd% --port=%~2"
    shift
    shift
    goto parse_args
)
if "%~1"=="--reload" (
    set "cmd=%cmd% --reload"
    shift
    goto parse_args
)
set "cmd=%cmd% %~1"
shift
goto parse_args

:start_server
echo 启动命令: %cmd%
echo 按Ctrl+C停止服务器
echo ================================

:: 执行命令
%cmd%