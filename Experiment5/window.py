import tkinter as tk
from tkinter import ttk, messagebox
from schedules import *


def draw_gantt_chart(canvas, tasks):
    y_offset = 40  # 每个任务的垂直间隔
    start_y = 50  # 初始 Y 位置
    x_scale = 20  # X轴缩放比例
    label_offset = 30  # 左侧任务标签的水平偏移

    # 绘制时间轴
    time_axis_y = start_y + len(tasks) * y_offset + 20
    canvas.create_line(50, time_axis_y, 600, time_axis_y, arrow=tk.LAST)
    for t in range(21):
        x = 50 + t * x_scale
        canvas.create_line(x, time_axis_y - 5, x, time_axis_y + 5)
        canvas.create_text(x, time_axis_y + 15, text=str(t), font=("Arial", 8))

    # 绘制每个任务的矩形块、编号和标签
    for i, (label, segments) in enumerate(tasks):
        y = start_y + i * y_offset  # 当前任务的 Y 位置

        # 在左侧绘制任务标签（A、B、C...）
        canvas.create_text(label_offset, y + y_offset / 2, text=label, font=("Arial", 12), anchor="e")

        # 绘制任务的每个段（矩形块）
        for (x, l) in segments:
            x1 = 50 + x * x_scale
            x2 = 50 + (x + l) * x_scale

            color = "cyan"
            canvas.create_rectangle(x1, y, x2, y + 20, fill=color, outline="black")

            # 在块内显示数字编号
            canvas.create_text((x1 + x2) / 2, y + 10, text=str(l), font=("Arial", 10))


# 创建 tkinter 主窗口
root = tk.Tk()
root.title("Gantt Chart")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

operation_var = tk.StringVar(value="Exit")
operation_label = ttk.Label(left_frame, text="Select Operation:")
operation_label.grid(row=10, column=0, pady=20)

operation_menu = ttk.Combobox(left_frame, textvariable=operation_var, state='readonly')
operation_menu['values'] = (
    'FCFS', 'SJF', 'SRTF', 'HRRF', 'Pr', 'RR', 'MLFQ', 'Exit'
)
operation_menu.grid(row=10, column=1, pady=20)


def quitf(*args, **kwargs):
    import sys
    root.quit()
    root.destroy()
    sys.exit(0)


def operation_menu_callback(event):
    switch = {
        'FCFS': FCFS,
        'SJF': SJF,
        'SRTF': SRTF,
        'HRRF': HRRF,
        'Pr': Pr,
        'RR': RR,
        'MLFQ': MLFQ,
        'Exit': quitf
    }
    func = switch.get(event.widget.get(), None)
    display(func, acquire_data())


def display(func, data):
    if data is None:
        return
    processes = []
    for pid, arrival_time, service_time, priority in data:
        process = Process(pid, int(arrival_time), int(service_time), int(priority))
        processes.append(process)
    processes = func(processes)
    tasks = [(p.pid, [(p.arrival_time, p.service_time)]) for p in processes]
    tasks.sort(key=lambda x: x[0])
    for p in processes:
        print(p.arrival_time, p.service_time, p.priority, p.pid)
    canvas.delete("all")
    draw_gantt_chart(canvas, tasks)


def acquire_data():
    data = []
    try:
        for row in rows:
            label = row[0].get()  # 获取任务名称
            start_time = int(row[1].get())  # 获取开始时间
            duration = int(row[2].get())  # 获取持续时间
            number = int(row[3].get())  # 获取优先数
            data.append((label, start_time, duration, number))
        return data
    except ValueError:
        messagebox.showerror("输入错误", "请确保所有数值字段都为整数。")
        return None


# 创建表头
headers = ["任务名称", "开始时间", "持续时间", "优先数"]
for col, header in enumerate(headers):
    tk.Label(left_frame, text=header, font=("Arial", 12)).grid(row=0, column=col, padx=5, pady=5)

# 创建表格
default_tasks = [
    ['A', '0', '3', '4'],
    ['B', '2', '6', '2'],
    ['C', '4', '4', '3'],
    ['D', '6', '5', '5'],
    ['E', '8', '2', '1']
]
rows = []
for i in range(5):
    row = []
    for j in range(4):
        entry = tk.Entry(left_frame, width=10, textvariable=tk.StringVar(value=default_tasks[i][j]))
        entry.grid(row=i+1, column=j, padx=5, pady=5)
        row.append(entry)
    rows.append(row)

operation_menu.bind("<<ComboboxSelected>>", operation_menu_callback)
canvas = tk.Canvas(right_frame, width=650, height=400, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

root.mainloop()
