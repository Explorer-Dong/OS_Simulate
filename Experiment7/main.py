r"""
This is the main window of the experiment.
To run the experiment, you can use either of the following commands in the terminal:
- g++ solution1.cpp -o solution.exe && ./solution.exe word1.txt word2.txt && python main.py
- g++ solution1.cpp -o solution.exe && ./solution.exe word1.txt word2.txt && python main.py
"""

import tkinter as tk


class Process:
    def __init__(self, data_arr):
        self.name = data_arr[0]
        self.time_sequence = data_arr[1:]
        self.name = self.name.split("$$")[1]
        self.time_sequence = list(map(int, self.time_sequence))
        self.idx = 0  # cnt = idx
        self.max_idx = len(self.time_sequence)

    @property
    def finished(self):
        return self.idx >= self.max_idx

    def run(self, time):
        while not self.finished and self.time_sequence[self.idx] <= time:
            self.idx += 1
        return self.name, self.idx, self.finished


class Counter:
    def __init__(self, data, step):
        self.processes = [Process(d.split()) for d in data]
        self.processes.sort(key=lambda p: p.name)
        self.step = step
        self.now = 0

    @property
    def finished(self):
        return all(p.finished for p in self.processes)

    def next_moment(self):
        if self.finished:
            return None
        self.now += self.step
        cnt = [p.run(self.now) for p in self.processes]
        return cnt

    @property
    def max_size(self):
        return max(p.max_idx for p in self.processes)


data = open('ans.out', 'r').readlines()
# print(data)
root = tk.Tk()
root.title("柱状图")
canvas_width = 1000
canvas_height = len(data) * 50 + 200  # 每行占50像素高度
root.geometry(f"1200x600")
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

x_offset = 100  # 起始X偏移量
y_offset = 100  # 起始Y偏移量
bar_height = 40  # 每个柱状图的高度


def display(counts, rate):
    canvas.delete("all")
    for i, (label, length, color_flag) in enumerate(counts):
        # 计算柱状图的长度（按比例缩放至画布宽度）
        bar_length = (canvas_width - 300) * rate * length
        color = "blue" if color_flag else "red"

        # 绘制标签
        canvas.create_text(x_offset - 20, y_offset + i * 50 + bar_height / 2, text=label, anchor="e")

        # 绘制柱状图
        canvas.create_rectangle(x_offset, y_offset + i * 50, x_offset + bar_length, y_offset + i * 50 + bar_height,
                                fill=color)
        # 在柱状图右侧显示长度
        canvas.create_text(x_offset + bar_length + 10, y_offset + i * 50 + bar_height / 2, text=str(length), anchor="w")


def display_animation(data):
    counter = Counter(data, 100)
    rate = 1 / (counter.max_size + 10)  # 缩放比例
    delay = 100  # 刷新时间（毫秒）
    while not counter.finished:
        counts = counter.next_moment()
        canvas.after(delay, display, counts, rate)
        delay += 100


button = tk.Button(root, text="开始动画", command=lambda: display_animation(data))
button.pack()
display_animation(data)
root.mainloop()
