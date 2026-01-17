import sounddevice as sd
import wave
import os
import tempfile
import requests
import pyperclip
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import ttk
from pynput import keyboard
from typing import Dict, Any

# 配置信息
CONFIG = {
    "audio_transcription_url": "https://lgy-in-dev.cnbita.com/cccadb63-d7fe-2559-ab62-c3b95a066a82/v1/audio/transcriptions",
    "audio_transcription_token": "sk-ouyJb7y6nXNR64ftd9cEdqQLLwb64FFhKfL9o6Em2xk2mkNL",
    "audio_transcription_model": "sensevoice"
}

# 全局变量
recording = False
frames = []
selected_device = 7 # 默认选择设备 7: Microphone (3- High Definition Audio Device)
float_window = None
status_label = None
animation_label = None

# 按键状态追踪
f9_pressed = False
keyboard_listener = None
recording_lock = threading.Lock()  # 添加锁来保护共享资源


def list_audio_devices():
    """列出可用的音频输入设备"""
    print("\n=== 可用的音频输入设备 ===")
    devices = sd.query_devices()
    input_devices = []
    
    for i, device in enumerate(devices):
        if device.get('max_input_channels', 0) > 0:
            input_devices.append((i, device.get('name')))
            print(f"设备 {i}: {device.get('name')}")
    
    return input_devices


def create_float_window():
    """创建悬浮窗"""
    global float_window, status_label, animation_label
    
    # 创建Tkinter窗口
    root = tk.Tk()
    root.title("语音转文字")
    
    # 设置窗口为置顶
    root.attributes('-topmost', True)
    
    # 移除窗口边框
    root.overrideredirect(True)
    
    # 设置窗口大小和位置
    window_width = 300
    window_height = 120
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = screen_width - window_width - 20
    y = screen_height - window_height - 100
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 设置窗口背景
    root.configure(bg='#2c3e50')
    
    # 创建标题标签
    title_label = ttk.Label(root, text="🎤 录音中...", 
                          font=('Microsoft YaHei', 14, 'bold'),
                          background='#2c3e50',
                          foreground='#ecf0f1')
    title_label.pack(pady=(15, 5))
    
    # 创建状态标签
    global status_label, animation_label
    status_label = ttk.Label(root, text="按 F9 停止录音", 
                           font=('Microsoft YaHei', 10),
                           background='#2c3e50',
                           foreground='#bdc3c7')
    status_label.pack(pady=5)
    
    # 创建动画效果
    animation_label = ttk.Label(root, text="",
                               font=('Microsoft YaHei', 12),
                               background='#2c3e50',
                               foreground='#3498db')
    animation_label.pack(pady=5)
    
    # 动画线程
    def animate():
        dots = ["", ".", "..", "..."]
        index = 0
        while float_window and root.winfo_exists():
            if animation_label is not None:
                try:
                    current_text = animation_label.cget("text")
                    if "正在录音" in current_text or "转写中" in current_text:
                        base_text = current_text.split("...")[0].split(".")[0].split("..")[0]
                        animation_label.config(text=f"{base_text}{dots[index]}")
                except tk.TclError:
                    # 如果组件已被销毁，则退出循环
                    break
            index = (index + 1) % 4
            try:
                if root.winfo_exists():
                    root.update_idletasks()
                else:
                    break  # 窗口不存在则退出
            except tk.TclError:
                break  # 如果更新失败，退出循环
            time.sleep(0.5)
    
    # 启动动画
    animation_thread = threading.Thread(target=animate)
    animation_thread.daemon = True
    animation_thread.start()
    
    float_window = root
    return root


def show_float_window():
    """显示悬浮窗"""
    global float_window
    
    print(f"[悬浮窗] 显示悬浮窗，当前float_window状态: {float_window}")
    
    # 如果已有悬浮窗存在，先隐藏它
    if float_window is not None:
        try:
            float_window.destroy()
        except:
            pass
        float_window = None
    
    print("[悬浮窗] 创建新的悬浮窗线程")
    
    # 在新线程中运行Tkinter
    def run_tk():
        print("[悬浮窗] 进入Tkinter线程")
        root = create_float_window()
        print("[悬浮窗] 悬浮窗已创建，进入主循环")
        root.mainloop()
        print("[悬浮窗] Tkinter主循环已退出")
    
    tk_thread = threading.Thread(target=run_tk)
    tk_thread.daemon = True
    tk_thread.start()
    # 等待窗口创建
    time.sleep(0.1)
    print("[悬浮窗] 悬浮窗线程已启动")


def update_float_window_status(status_text, animation_text):
    """更新悬浮窗状态"""
    global float_window, status_label, animation_label
    
    print(f"[悬浮窗更新] 尝试更新状态，float_window: {float_window}, status_label: {status_label}, animation_label: {animation_label}")
    if float_window is not None:
        print(f"[悬浮窗更新] 执行更新，状态: {status_text}, 动画: {animation_text}")
        # 在Tkinter主线程中更新UI
        if status_label is not None and animation_label is not None:
            float_window.after(0, lambda: status_label.config(text=status_text) if status_label else None)
            float_window.after(0, lambda: animation_label.config(text=animation_text) if animation_label else None)
        print("[悬浮窗更新] 更新已提交")
    else:
        print("[悬浮窗更新] 悬浮窗不存在，无法更新")


def hide_float_window():
    """隐藏悬浮窗"""
    global float_window
    
    print(f"[悬浮窗隐藏] 尝试隐藏悬浮窗，当前float_window状态: {float_window}")
    if float_window is not None:
        print("[悬浮窗隐藏] 执行销毁操作")
        try:
            # 直接销毁窗口，不使用after方法
            float_window.destroy()
            float_window = None
            print("[悬浮窗隐藏] 窗口已销毁")
        except Exception as e:
            print(f"[悬浮窗隐藏] 销毁窗口失败: {e}")
            float_window = None
    else:
        print("[悬浮窗隐藏] 悬浮窗不存在，无需销毁")
    
    # 确保销毁后添加短暂延时，让日志有时间输出
    time.sleep(0.05)


def on_key_press(key):
    """键盘按键按下事件处理"""
    global f9_pressed
    
    try:
        print(f"[按键检测] 检测到按键: {key}, f9_pressed={f9_pressed}, recording={recording}")
        if key == keyboard.Key.f9:
            if not f9_pressed:
                f9_pressed = True
                print(f"[按键处理] F9键按下，触发处理，当前recording状态: {recording}")
                # 开启新线程处理逻辑，避免阻塞监听器
                threading.Thread(target=on_f9_logic_trigger, daemon=True).start()
    except AttributeError as e:
        print(f"[按键错误] 检测错误: {e}")


def on_key_release(key):
    """键盘按键释放事件处理"""
    global f9_pressed
    
    try:
        if key == keyboard.Key.f9:
            f9_pressed = False  # 释放按键后立即重置，允许下次触发
            print(f"[按键释放] F9键释放，f9_pressed已重置")
    except AttributeError:
        pass

def on_f9_logic_trigger():
    """处理录音开关逻辑，不再阻塞监听线程"""
    global recording, frames
    
    with recording_lock:
        if not recording:
            # --- 开始录音逻辑 ---
            recording = True
            frames = []
            show_float_window()
            threading.Thread(target=record_audio, daemon=True).start()
            print("[系统] 开始录音...")
        else:
            # --- 停止录音逻辑 ---
            recording = False
            print("[系统] 停止录音，准备转写...")
            update_float_window_status("正在转写音频...", "转写中")
    
    # 【关键】将耗时操作移出 recording_lock 锁之外
    if not recording:
        process_transcription_flow()

def process_transcription_flow():
    """独立的转写处理流程"""
    try:
        time.sleep(0.3) # 留出时间让录音回调彻底停止
        audio_file_path = save_audio()
        if audio_file_path:
            text = transcribe_audio(audio_file_path)
            if text:
                copy_to_clipboard(text)
                paste_to_active_window()
                print(f"完成: {text}")
            
            # 清理
            if os.path.exists(audio_file_path):
                os.unlink(audio_file_path)
    finally:
        # 无论成功失败，最后隐藏窗口
        hide_float_window()


def set_keyboard_hook():
    """设置键盘监听器"""
    global keyboard_listener
    
    # 创建键盘监听器
    keyboard_listener = keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release
    )
    
    # 启动监听器
    keyboard_listener.start()
    
    return True


def remove_keyboard_hook():
    """移除键盘监听器"""
    global keyboard_listener
    
    if keyboard_listener:
        keyboard_listener.stop()
        keyboard_listener = None


def select_audio_device():
    """选择音频输入设备"""
    global selected_device
    
    input_devices = list_audio_devices()
    
    if not input_devices:
        print("错误: 未找到音频输入设备")
        return None
    
    print("\n请选择要使用的音频设备:")
    print("1. 通过设备编号选择")
    print("2. 通过设备名称选择")
    
    try:
        mode = int(input("请选择模式(1或2): "))
        
        if mode == 1:
            choice = int(input("请输入设备编号: "))
            if 0 <= choice < len(input_devices):
                selected_device = choice
                print(f"已选择设备: {input_devices[choice][1]}")
                return choice
            else:
                print("错误: 无效的设备编号")
                return None
        
        elif mode == 2:
            device_name = input("请输入设备名称(可以是部分名称): ")
            matched_devices = [(i, name) for i, name in input_devices if device_name.lower() in name.lower()]
            
            if len(matched_devices) == 0:
                print("错误: 未找到匹配的设备")
                return None
            elif len(matched_devices) == 1:
                selected_device = matched_devices[0][0]
                print(f"已选择设备: {matched_devices[0][1]}")
                return selected_device
            else:
                print("\n找到多个匹配的设备:")
                for i, (device_id, name) in enumerate(matched_devices):
                    print(f"{i}: {name}")
                
                sub_choice = int(input("请选择设备编号: "))
                if 0 <= sub_choice < len(matched_devices):
                    selected_device = matched_devices[sub_choice][0]
                    print(f"已选择设备: {matched_devices[sub_choice][1]}")
                    return selected_device
                else:
                    print("错误: 无效的设备编号")
                    return None
        
        else:
            print("错误: 无效的选择模式")
            return None
            
    except ValueError:
        print("错误: 请输入有效的数字")
        return None


def record_audio():
    """录制音频"""
    global recording, frames, selected_device
    
    # 音频参数（与系统录音机匹配）
    sample_rate = 44100
    
    # 获取设备支持的通道数
    device_info = sd.query_devices(selected_device)
    # 直接转换为整数以满足类型检查器
    channels = min(int(float(device_info['max_input_channels'])), 2)  # 最多使用2通道
    print(f"使用设备 {selected_device}，通道数: {channels}")
    
    def callback(indata, frames_count, time_info, status):
        """录音回调函数"""
        if recording:
            frames.append(indata.copy())
    
    # 开始录音
    print("开始录音...")
    # 使用dtype='int16'以获得更好的音频质量（与WAV格式兼容）
    # 使用selected_device指定录音设备
    with sd.InputStream(callback=callback, channels=channels, samplerate=sample_rate, 
                       dtype='int16', device=selected_device):
        while recording:
            sd.sleep(100)


def save_audio():
    """保存音频到临时文件"""
    global frames
    
    if not frames:
        return None
    
    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_file_path = temp_file.name
    temp_file.close()
    
    # 保存音频（与系统录音机参数匹配）
    sample_rate = 44100
    
    # 从frames中获取实际的通道数
    if frames:
        channels = frames[0].shape[1] if len(frames[0].shape) > 1 else 1
    else:
        channels = 1
    
    print(f"保存音频，通道数: {channels}")
    
    with wave.open(temp_file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wf.setframerate(sample_rate)
        wf.setcomptype('NONE', 'not compressed')  # 无压缩
        
        # 确保数据格式正确
        if frames:
            # 如果使用dtype='int16'，数据已经是正确的格式
            if frames[0].dtype == 'int16':
                wf.writeframes(b''.join(frames))
            else:
                # 转换为int16格式
                import numpy as np
                audio_data = np.concatenate(frames, axis=0)
                audio_data = (audio_data * 32767).astype('int16')
                wf.writeframes(audio_data.tobytes())
    
    print(f"音频已保存到: {temp_file_path}")
    return temp_file_path


def transcribe_audio(audio_file_path):
    """调用API转写音频"""
    url = CONFIG["audio_transcription_url"]
    token = CONFIG["audio_transcription_token"]
    model = CONFIG["audio_transcription_model"]
    
    if not url or not token or not model:
        print("错误: 配置不完整")
        return None
    
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Authorization': f'Bearer {token}',
        'Connection': 'keep-alive',
        'User-Agent': 'PostmanRuntime-ApipostRuntime/1.1.0',
    }
    
    try:
        with open(audio_file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(audio_file_path), f, 'audio/wav'),
                'model': (None, model)
            }
            print("正在调用语音转文字API...")
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()  # 检查HTTP错误
            result = response.json()
            print(f"转写结果: {result}")
            
            if result and 'text' in result:
                return result['text']
            else:
                print("错误: 未从API获取到文本结果")
                return None
    except Exception as e:
        print(f"调用API失败: {e}")
        return None


def copy_to_clipboard(text):
    """复制文本到剪贴板"""
    try:
        pyperclip.copy(text)
        print("转写结果已复制到剪贴板")
        return True
    except Exception as e:
        print(f"复制到剪贴板失败: {e}")
        return False


def paste_to_active_window():
    """粘贴到当前活动窗口"""
    try:
        # 模拟Ctrl+V粘贴操作
        pyautogui.hotkey('ctrl', 'v')
        print("已尝试粘贴到当前活动窗口")
        return True
    except Exception as e:
        print(f"粘贴失败: {e}")
        return False





def main():
    """主函数"""
    print("=== 语音转文字工具 ===")
    
    # 显示默认选择的设备
    print(f"\n默认使用设备 {selected_device}: 麦克风 (HD Audio Microphone)")
    print("如果需要更改设备，请修改代码中的 selected_device 变量")
    
    print("\n按F9键开始录音，再次按F9键停止录音")
    print("转写结果将自动复制到剪贴板并尝试粘贴到当前活动窗口")
    print("按Ctrl+C退出程序")
    
    # 设置键盘监听器
    if not set_keyboard_hook():
        print("错误: 无法启动键盘监听")
        return
    
    print("\n键盘监听器已设置，正在监听F9键...")
    
    # 保持程序运行
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        # 移除键盘监听器
        remove_keyboard_hook()
        print("\n程序已退出")


if __name__ == "__main__":
    main()
