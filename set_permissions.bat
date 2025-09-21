@echo off
echo 给Git Bash启动脚本添加执行权限...
icacls "start_with_git_bash.sh" /grant Everyone:RX
echo 完成！
pause