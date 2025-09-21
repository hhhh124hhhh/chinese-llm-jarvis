@echo off
echo 清理Git Bash残留环境配置...

:: 清除Git Bash相关的环境变量
set TMPDIR=
set TEMP=%SystemRoot%\TEMP
set TMP=%SystemRoot%\TEMP

:: 清除可能存在的Git Bash路径变量
set GIT_BASH_PATH=
set CYGWIN=
set MSYS=
set SHELLOPTS=
set BASH_ENV=

echo 环境变量已清理
echo 现在可以正常使用Windows命令行了

:: 测试基本命令
echo 测试Python安装...
python --version

echo 测试uv安装...
uv --version

pause