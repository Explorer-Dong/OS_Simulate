import tkinter as tk
from tkinter import ttk, messagebox
from schedules import *
import numpy as np


def draw_bar(canvas, array, canvas_height, xoffset=0, xscale=20):
    last_color = None
    start_index = 0
    for i, value in enumerate(array):
        if value == -1:
            if last_color is not None:
                x0 = start_index * xscale + xoffset
                x1 = i * xscale + xoffset
                canvas.create_rectangle(x0, canvas_height - 20, x1, canvas_height, fill=last_color)
                length = i - start_index
                mid_x = (x0 + x1) / 2
                canvas.create_text(mid_x, canvas_height - 10, text=str(length), fill='black')
                last_color = None
            continue

        current_color = 'gray' if value == 0 else 'cyan'

        if last_color is None:
            last_color = current_color
            start_index = i
        elif current_color != last_color:
            x0 = start_index * xscale + xoffset
            x1 = i * xscale + xoffset
            canvas.create_rectangle(x0, canvas_height - 20, x1, canvas_height, fill=last_color)
            length = i - start_index
            mid_x = (x0 + x1) / 2
            canvas.create_text(mid_x, canvas_height - 10, text=str(length), fill='black')
            last_color = current_color
            start_index = i

    if last_color is not None:
        x0 = start_index * xscale + xoffset
        x1 = len(array) * xscale + xoffset
        canvas.create_rectangle(x0, canvas_height - 20, x1, canvas_height, fill=last_color)
        length = len(array) - start_index
        mid_x = (x0 + x1) / 2
        canvas.create_text(mid_x, canvas_height - 10, text=str(length), fill='black')


def draw_bar_with_animation(canvas, tasks, canvas_height=40, delay=500):
    """
    动态绘制柱状图
    :param canvas: Tkinter 画布
    :param array: 数组数据
    :param canvas_height: 画布高度
    :param delay: 每步的延迟时间，毫秒
    """
    # 清空画布
    canvas.delete("all")
    pid, time_sequence = [], []
    [(pid.append(task[0]), time_sequence.append(task[1])) for task in tasks]

    x_scale = 25  # X轴缩放比例

    # 绘制时间轴
    time_axis_y = 50 + len(tasks) * canvas_height + 20
    canvas.create_line(50, time_axis_y, 800, time_axis_y, arrow=tk.LAST)
    for t in range(21):
        x = 50 + t * x_scale
        canvas.create_line(x, time_axis_y - 5, x, time_axis_y + 5)
        canvas.create_text(x, time_axis_y + 15, text=str(t), font=("Arial", 8))

    # 绘制任务名称
    for i, label in enumerate(pid):
        y = 50 + (i + 1) * canvas_height - 10
        canvas.create_text(30, y, text=label, font=("Arial", 12), anchor="e")

    # 绘制甘特图
    for i in range(max([t.shape[0] for t in time_sequence])):
        for j in range(len(tasks)):
            canvas.after(delay * i, draw_bar, canvas, time_sequence[j][:i], 50 + canvas_height * (j + 1), 50, x_scale)


# 创建 tkinter 主窗口
def init():
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
    return root, left_frame, right_frame, operation_menu


def quitf(root, *args, **kwargs):
    import sys
    root.quit()
    root.destroy()
    sys.exit(0)


def operation_menu_callback(event, table_rows, canvas):
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
    display(func, acquire_data(table_rows), canvas)


def transform_array(pairs):
    max_index = max(start + length for start, length in pairs)
    result = np.full(max_index + 1, -1)
    last = -1
    for start, length in pairs:
        if last != -1:
            result[last:start] = 0
        last = start + length
        result[start:last] = 1
    return result


def display(func, data, canvas):
    if data is None:
        return
    processes = []
    for pid, arrival_time, service_time, priority in data:
        process = Process(pid, int(arrival_time), int(service_time), int(priority))
        processes.append(process)
    processes = func(processes)
    tasks = [(p.pid, transform_array([(p.arrival_time, 0)] + p.start_time)) for p in processes]
    tasks.sort(key=lambda x: x[0])
    # print([(p.pid, [(p.arrival_time, p.arrival_time)] + p.start_time) for p in processes])
    # print(tasks)
    draw_bar_with_animation(canvas, tasks)


def acquire_data(table_rows):
    data = []
    try:
        for row in table_rows:
            label = row[0].get()  # 获取任务名称
            start_time = int(row[1].get())  # 获取开始时间
            duration = int(row[2].get())  # 获取持续时间
            number = int(row[3].get())  # 获取优先数
            data.append((label, start_time, duration, number))
        return data
    except ValueError:
        messagebox.showerror("输入错误", "请确保所有数值字段都为整数。")
        return None


def create_table(left_frame):
    rows = []
    # 创建表头
    headers = ["任务名称", "到达时间", "估算时间", "优先数"]
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
    for i in range(5):
        row = []
        for j in range(4):
            entry = tk.Entry(left_frame, width=10, textvariable=tk.StringVar(value=default_tasks[i][j]))
            entry.grid(row=i + 1, column=j, padx=5, pady=5)
            row.append(entry)
        rows.append(row)
    return rows


# 主函数
def MainWindow():
    root, left_frame, right_frame, operation_menu = init()
    table_rows = create_table(left_frame)
    canvas = tk.Canvas(right_frame, width=650, height=400, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)
    operation_menu.bind(
        "<<ComboboxSelected>>",
        lambda event: operation_menu_callback(event, table_rows, canvas)
    )
    return root


if __name__ == "__main__":
    MainWindow().mainloop()
