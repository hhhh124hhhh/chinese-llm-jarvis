#!/bin/bash
# 简单的Git Bash环境修复
export TMPDIR="/tmp"
export TEMP="/tmp"  
export TMP="/tmp"

# 解决cygpath问题
if ! command -v cygpath &> /dev/null; then
    cygpath() { echo "$2"; }
    export -f cygpath
fi

echo "Git Bash环境已修复，现在可以运行命令了"