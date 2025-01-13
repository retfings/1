import json
import time
import pyautogui
import random

config_file = 'click_points.json'

def load_click_points():
    """从JSON文件中读取点击点"""
    with open(config_file, 'r') as file:
        click_points = json.load(file)
    return click_points

def perform_click_simulation():
    """每隔十分钟选择一个随机的点击点进行模拟点击"""
    while True:
        click_points = load_click_points()
        selected_point = random.choice(click_points)
        pyautogui.click(selected_point['x'], selected_point['y'])
        print(f"点击点: x={selected_point['x']}, y={selected_point['y']}")
        time.sleep(5)  # 每10分钟点击一次

# 运行点击模拟
perform_click_simulation()
