@echo off
chcp 65001 >nul
echo ========================================
echo    语音转文字工具 - 安装向导
echo ========================================
echo.
echo 步骤1: 打包Python程序为可执行文件...
python setup.py build
echo.
echo 步骤2: 创建开始菜单快捷方式...
python create_startmenu_shortcut.py
echo.
echo 步骤3: 创建开机自启动快捷方式...
python create_startup_shortcut.py
echo.
echo ========================================
echo    安装完成！
echo ========================================
echo.
echo 程序已安装到以下位置:
echo   - 可执行文件: build\exe.win-amd64-3.12\AudioTranscriptionTool.exe
echo   - 开始菜单: 开始菜单 > 所有程序 > AudioTranscriptionTool
echo   - 开机自启动: 已添加到开机启动项
echo.
echo 使用方法:
echo   1. 按F9键开始录音
echo   2. 再次按F9键停止录音
echo   3. 转写结果会自动复制到剪贴板并尝试粘贴到当前活动窗口
echo   4. 按Ctrl+C退出程序
echo.
pause
