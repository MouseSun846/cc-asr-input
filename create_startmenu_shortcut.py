import os
import winshell
from win32com.client import Dispatch

def create_startmenu_shortcut():
    """创建开始菜单快捷方式"""
    
    # 获取当前脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 可执行文件路径
    exe_path = os.path.join(script_dir, "build", "exe.win-amd64-3.12", "AudioTranscriptionTool.exe")
    
    # 检查可执行文件是否存在
    if not os.path.exists(exe_path):
        print(f"错误: 可执行文件不存在: {exe_path}")
        print("请先运行 build.bat 打包程序")
        return False
    
    # 获取开始菜单程序目录
    startmenu_dir = os.path.join(winshell.programs(), "AudioTranscriptionTool")
    print(f"开始菜单程序目录: {startmenu_dir}")Yeah.
    # 创建程序文件夹（如果不存在）
    if not os.path.exists(startmenu_dir):
        os.makedirs(startmenu_dir)
    
    # 快捷方式名称
    shortcut_name = "语音转文字工具.lnk"
    shortcut_path = os.path.join(startmenu_dir, shortcut_name)
    
    # 创建快捷方式
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.Description = "语音转文字工具 - 按F9开始/停止录音"
    shortcut.IconLocation = exe_path  # 使用可执行文件的图标
    shortcut.save()
    
    print(f"开始菜单快捷方式已创建: {shortcut_path}")
    return True

if __name__ == "__main__":
    create_startmenu_shortcut()
