import json
import time
from Quartz.CoreGraphics import (CGEventTapCreate, kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGEventTapDisabledByTimeout, kCGEventTapEnabledByTimeout, kCGEventTapOptionListenOnly, kCGEventTapOptionDefault, kCGEventLeftMouseDragged, kCGEventMouseMoved, kCGEventType)
from Quartz.CoreGraphics import (kCGEventTapEventDown, kCGEventMouseDragged, kCGEventTypeMouse, kCGEventMouseMoved)

click_points = []
config_file = 'click_points.json'

def event_callback(proxy, type, event, refcon):
    """事件回调处理"""
    if type == kCGEventLeftMouseDown:
        pos = event.location
        click_points.append({"x": pos.x, "y": pos.y})
        print(f"记录点击点: x={pos.x}, y={pos.y}")
        if len(click_points) >= 20:
            with open(config_file, 'w') as file:
                json.dump(click_points, file, indent=4)
            print(f"{len(click_points)}个点击点已保存到 {config_file}")
            return False  # 停止监听
    return True

def record_clicks(n=20):
    """记录用户点击的n个点击点并保存到JSON文件中"""
    print(f"请在屏幕上点击鼠标，将记录您的点击位置 (最多 {n} 次点击)。")
    
    event_mask = (1 << kCGEventLeftMouseDown)
    event_tap = CGEventTapCreate(kCGEventTapOptionDefault, event_mask)
    
    run_loop = CFRunLoopGetCurrent()
    CFRunLoopAddSource(run_loop, event_tap, kCFRunLoopCommonModes)
    event_tap.startListening(event_callback)

# 运行示例
record_clicks()
