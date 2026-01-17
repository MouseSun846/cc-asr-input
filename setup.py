import sys
from cx_Freeze import setup, Executable

# 要打包的Python文件
script_name = "audio_transcription_tool.py"

# 可执行文件配置
base = None
# if sys.platform == "win32":
#     base = "Win32GUI"  # 使用GUI模式，不显示控制台窗口

# 可执行文件设置
executables = [
    Executable(
        script=script_name,
        base=base,
        target_name="AudioTranscriptionTool.exe",
        icon=None  # 如果有图标文件，可以在这里指定
    )
]

# 打包配置
setup(
    name="AudioTranscriptionTool",
    version="1.0",
    description="语音转文字工具",
    executables=executables,
    options={
        "build_exe": {
            "packages": ["pynput", "sounddevice", "wave", "os", "tempfile", "requests", "pyperclip", "pyautogui", "time", "threading", "shutil", "numpy", "tkinter"],
            "include_files": [],
            "excludes": [],
            "optimize": 0
        }
    }
)
