import json
import Quartz

# 定义点击点的存储文件
config_file = 'click_points.json'
click_points = []

def get_mouse_position():
    """获取当前鼠标位置"""
    event = Quartz.CGEventCreate(None)
    point = Quartz.CGEventGetLocation(event)
    return point.x, point.y

def monitor_mouse_clicks():
    """监听鼠标点击事件并记录点击位置"""
    def callback(proxy, event_type, event, refcon):
        if event_type == Quartz.kCGEventLeftMouseDown:
            x, y = get_mouse_position()
            # 将点击位置添加到列表中
            click_points.append({"x": x, "y": y})
            print(f"记录点击点: x={x}, y={y}")

            # 如果列表长度超过 20，移除最旧的事件
            if len(click_points) > 20:
                click_points.pop(0)

            # 实时保存到 JSON 文件
            with open(config_file, 'w') as file:
                json.dump(click_points, file, indent=4)
            print(f"{len(click_points)}个点击点已保存到 {config_file}")

            # 如果记录达到 20 个点击点，停止监听
            if len(click_points) >= 20:
                Quartz.CFRunLoopStop(Quartz.CFRunLoopGetCurrent())

        return event

    # 创建一个事件点击监听器
    event_mask = (1 << Quartz.kCGEventLeftMouseDown)  # 监听左键点击事件
    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,  # 监听会话级别的事件
        Quartz.kCGHeadInsertEventTap,  # 插入到事件流的头部
        Quartz.kCGEventTapOptionDefault,  # 默认选项
        event_mask,
        callback,
        None
    )

    if tap is None:
        print("Failed to create event tap")
        return

    # 创建一个运行循环源并添加到当前运行循环
    run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    Quartz.CFRunLoopAddSource(
        Quartz.CFRunLoopGetCurrent(),
        run_loop_source,
        Quartz.kCFRunLoopCommonModes
    )

    # 启用事件点击
    Quartz.CGEventTapEnable(tap, True)

    # 运行循环
    print("请在屏幕上点击鼠标，将记录您的点击位置 (最多 20 次点击)。")
    Quartz.CFRunLoopRun()

if __name__ == "__main__":
    monitor_mouse_clicks()