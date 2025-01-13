import Quartz

# 用于存储鼠标点击位置的列表
click_positions = []

def get_mouse_position():
    # 获取当前鼠标位置
    event = Quartz.CGEventCreate(None)
    point = Quartz.CGEventGetLocation(event)
    return point.x, point.y

def monitor_mouse_clicks():
    # 创建一个事件点击回调函数
    def callback(proxy, event_type, event, refcon):
        if event_type == Quartz.kCGEventLeftMouseDown:
            x, y = get_mouse_position()
            # 将点击位置添加到列表中
            click_positions.append((x, y))
            # 如果列表长度超过 20，移除最旧的事件
            if len(click_positions) > 20:
                click_positions.pop(0)
            print(f"Mouse clicked at: ({x}, {y})")
            print(f"Recent clicks (max 20): {click_positions}")
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
    Quartz.CFRunLoopRun()

if __name__ == "__main__":
    monitor_mouse_clicks()