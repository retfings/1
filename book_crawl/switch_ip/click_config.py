import json
import time
import pyautogui
from pynput import mouse

# 定义点击点的存储文件
config_file = 'click_points.json'
click_points = []

def on_click(x, y, button, pressed):
    """鼠标点击事件处理"""
    if pressed:
        click_points.append({"x": x, "y": y})
        print(f"记录点击点: x={x}, y={y}")
        if len(click_points) >= 20:
            with open(config_file, 'w') as file:
                json.dump(click_points, file, indent=4)
            print(f"{len(click_points)}个点击点已保存到 {config_file}")
            return False  # 停止监听

def record_clicks(n=20):
    """记录用户点击的n个点击点并保存到JSON文件中"""
    print(f"请在屏幕上点击鼠标，将记录您的点击位置 (最多 {n} 次点击)。")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

# 运行示例
record_clicks()