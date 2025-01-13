# import json
# from Quartz.CoreGraphics import (CGEventTapCreate, 
#                                   kCGEventLeftMouseDown, 
#                                   kCGEventLeftMouseUp, 
#                                   kCGEventTapOptionDefault, 
#                                   kCGEventTapEventTap)
# from Quartz.CoreGraphics import (CGEventTapEnable, 
#                                   kCGEventTapOptionListenOnly)
# import Quartz.CoreGraphics as CG
# from AppKit import NSEvent, NSApplication
# import time

# # 定义点击点的存储文件
# config_file = 'click_points.json'
# click_points = []

# def event_callback(proxy, type, event, refcon):
#     """事件回调处理"""
#     if type == kCGEventLeftMouseDown:
#         pos = event.location
#         click_points.append({"x": pos.x, "y": pos.y})
#         print(f"记录点击点: x={pos.x}, y={pos.y}")
#         if len(click_points) >= 20:
#             # 保存点击点到文件
#             with open(config_file, 'w') as file:
#                 json.dump(click_points, file, indent=4)
#             print(f"{len(click_points)}个点击点已保存到 {config_file}")
#             return False  # 停止监听
#     return True

# def record_clicks(n=20):
#     """记录用户点击的n个点击点并保存到JSON文件中"""
#     print(f"请在屏幕上点击鼠标，将记录您的点击位置 (最多 {n} 次点击)。")
    
#     # 创建事件监听器
#     event_mask = (1 << kCGEventLeftMouseDown) | (1 << kCGEventLeftMouseUp)
#     event_tap = CG.CGEventTapCreate(
#         kCGEventTapOptionDefault,
#         kCGEventTapEventTap,
#         event_mask,
#         event_callback,
#         None
#     )

#     if not event_tap:
#         print("无法创建事件监听器!")
#         return

#     # 启动事件监听
#     event_tap.enable()
    
#     # 启动主运行循环
#     CFRunLoopRun()

# # 运行示例
# record_clicks()
