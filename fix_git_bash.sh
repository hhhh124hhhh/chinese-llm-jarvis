#!/bin/bash
# Git Bash环境修复脚本

# 解决cygpath缺失问题
if ! command -v cygpath &> /dev/null; then
    echo "cygpath not found, creating workaround..."
    
    # 创建cygpath的替代函数
    cygpath() {
        case "$1" in
            -u|--unix)
                echo "$2" | sed 's/\\/\//g' | sed 's/^C:/\/c/' | sed 's/^D:/\/d/' | sed 's/^E:/\/e/' | sed 's/^F:/\/f/'
                ;;
            -w|--windows)
                echo "$2" | sed 's/^\///' | sed 's/^c\//C:\//' | sed 's/^d\//D:\//' | sed 's/^e\//E:\//' | sed 's/^f\//F:\//' | sed 's/\//\\/g'
                ;;
            *)
                echo "$1"
                ;;
        esac
    }
    
    export -f cygpath
fi

# 设置临时目录的Windows路径
export TMPDIR="/tmp"
export TEMP="/tmp"
export TMP="/tmp"

echo "Git Bash环境修复完成"