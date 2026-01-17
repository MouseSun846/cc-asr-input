# CC-ASR-Input 语音输入助手

![公众号二维码](images/qrcode_for_gh_4d02030783b8_344.jpg)

*公众号：光影织梦*

一款适用于任意程序的通用语音输入软件，支持通过快捷键快速将语音转换为文字并自动输入到当前活动窗口。特别优化用于 Claude-Code 等编程辅助工具。

## 功能特性

- **全局快捷键录音**：按F9键开始录音，再次按F9键停止录音
- **自动转写**：录音完成后自动调用API进行语音转文字
- **智能粘贴**：转写结果自动复制到剪贴板，并尝试粘贴到当前活动窗口
- **悬浮窗提示**：录音和转写过程中显示悬浮窗提示状态
- **开机自启动**：支持设置开机自启动，方便随时使用
- **一键安装**：提供install.bat脚本，自动完成打包和安装
- **通用适配**：适用于任意程序的语音输入，特别优化用于 Claude-Code

## 技术栈

- **Python 3.12**：核心开发语言
- **sounddevice**：音频录制库
- **pynput**：全局键盘监听
- **Tkinter**：悬浮窗界面
- **requests**：API调用
- **pyperclip**：剪贴板操作
- **pyautogui**：自动粘贴
- **cx_Freeze**：打包成EXE

## 安装步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 一键安装（推荐）

```bash
install.bat
```

**install.bat 功能说明：**
- 自动打包Python程序为可执行文件
- 创建开始菜单快捷方式
- 创建开机自启动快捷方式

**安装完成后：**
- 可执行文件位置: `build\exe.win-amd64-3.12\AudioTranscriptionTool.exe`
- 开始菜单: 开始菜单 > 所有程序 > AudioTranscriptionTool
- 开机自启动: 已添加到开机启动项

### 3. 手动运行（开发调试）

```bash
python audio_transcription_tool.py
```

### 4. 手动打包

```bash
python setup.py build
```

打包后的可执行文件位于 `build/exe.win-amd64-3.12/AudioTranscriptionTool.exe`

## 使用说明

1. **启动程序**：运行程序后，控制台会显示设备信息和使用说明
2. **开始录音**：按F9键开始录音，悬浮窗会显示在屏幕右侧
3. **停止录音**：再次按F9键停止录音，悬浮窗显示"转写中..."
4. **查看结果**：转写完成后，结果会自动复制到剪贴板并尝试粘贴到当前窗口
5. **退出程序**：按Ctrl+C退出程序

## 配置说明

### 环境变量配置

程序需要设置以下环境变量：

```bash
# API配置 - 符合OpenAI /v1/audio接口标准
AUDIO_TRANSCRIPTION_URL=https://your-api-domain.com/v1/audio/transcriptions
AUDIO_TRANSCRIPTION_TOKEN=your-api-token
AUDIO_TRANSCRIPTION_MODEL=sensevoice
```

#### Windows (命令行)
```bash
set AUDIO_TRANSCRIPTION_URL=https://your-api-domain.com/v1/audio/transcriptions
set AUDIO_TRANSCRIPTION_TOKEN=your-api-token
set AUDIO_TRANSCRIPTION_MODEL=sensevoice
```

#### Windows (PowerShell)
```powershell
$env:AUDIO_TRANSCRIPTION_URL="https://your-api-domain.com/v1/audio/transcriptions"
$env:AUDIO_TRANSCRIPTION_TOKEN="your-api-token"
$env:AUDIO_TRANSCRIPTION_MODEL="sensevoice"
```

#### 永久设置（推荐）
1. 右键"此电脑" → 属性
2. 高级系统设置 → 环境变量
3. 在系统变量中添加上述环境变量

### 设备选择

在代码中修改 `selected_device` 变量来选择音频输入设备：

```python
selected_device = 7  # 默认选择设备7
```

运行程序时会列出所有可用的音频输入设备，你可以根据需要修改设备编号。

### API兼容性

本程序兼容符合OpenAI `/v1/audio/transcriptions` 接口标准的API服务，包括但不限于：
- OpenAI Whisper API
- SenseVoice API
- 其他兼容OpenAI接口的语音转文字服务

## 项目结构

```
.
├── audio_transcription_tool.py  # 主程序文件
├── setup.py                     # 打包配置
├── build.bat                    # 打包脚本
├── install.bat                  # 安装脚本
├── requirements.txt             # 依赖列表
└── README.md                    # 项目说明
```

## 注意事项

- 确保系统有可用的音频输入设备（麦克风）
- 确保网络连接正常，以便调用语音转文字API
- 首次使用可能需要授予程序访问麦克风的权限
- 建议使用高质量麦克风以获得更好的转写效果

## 常见问题

### Q: 为什么按F9键没有反应？
A: 请确保程序正在运行，并且焦点不在程序窗口上（全局快捷键需要在其他窗口测试）。

### Q: 转写结果不准确怎么办？
A: 请尝试：
- 使用质量更好的麦克风
- 在安静的环境中录音
- 说话清晰、语速适中
- 检查网络连接是否稳定

### Q: 如何更改录音设备？
A: 在代码中修改 `selected_device` 变量，运行程序时会列出所有可用设备。

## 更新日志

### v1.0.0 (2026-01-17)
- ✨ 实现核心录音和转写功能
- ✨ 添加全局F9快捷键控制
- ✨ 实现悬浮窗界面
- ✨ 支持自动复制粘贴
- ✨ 打包成EXE可执行文件
- ✨ 修复键盘监听稳定性问题
- ✨ 优化音频录制质量

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎反馈。

## 许可证

MIT License
