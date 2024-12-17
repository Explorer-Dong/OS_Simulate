import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Iterable
import pandas as pd


class Visualization(object):
    def __init__(self, master, realPageNumber=64, pageSize=1000):
        self.realPageNumber = realPageNumber
        self.pageSize = pageSize
        self.master = master

        self.memory_canvas = tk.Canvas(self.master, width=300, height=300)
        self.memory_canvas.pack(side=tk.LEFT, padx=10, pady=5)
        self.draw_memory()

        canvas = tk.Canvas(self.master, width=100, height=724)
        canvas.pack(side=tk.LEFT)
        self.page_canvas = [
            tk.Canvas(canvas, width=120, height=724, bg="white")
            for i in range(6)
        ]
        [c.pack(side=tk.LEFT, padx=10, pady=5) for c in self.page_canvas]
        self.id_dict = {}

    def init_page(self, canvas_number):
        canvas = self.page_canvas[canvas_number]
        canvas.create_rectangle(
            10, 10, 110, 714,
        )
        id_list = []
        for i in range(64):
            canvas.create_line(
                10, 10 + i * 11,
                110, 10 + i * 11,
            )
            text_id = canvas.create_text(
                60, 15 + i * 11,
                text=str(i),
                font=("Arial", 7),
            )
            id_list.append(text_id)
        self.id_dict[canvas_number] = id_list

    def update_page(self, canvas_number: int, record_list: Iterable):
        id_list = self.id_dict[canvas_number]
        for i, record in enumerate(record_list):
            self.page_canvas[canvas_number].itemconfig(
                id_list[i], text=str(record)
            )

    def clear_page(self, canvas_number: int):
        self.page_canvas[canvas_number].delete("all")
        self.id_dict[canvas_number] = []

    def draw_memory(self):
        self.memory_canvas.delete("all")
        width, height = 30, 30
        self.rectangles = pd.DataFrame(
            index=range(8),
            columns=range(8),
        )
        for k in range(self.realPageNumber):
            j, i = divmod(k, 8)
            x = i * width + 50
            y = j * height + 50
            rect_id = self.memory_canvas.create_rectangle(
                x, y, x + width, y + height, fill="sky blue",
            )
            self.rectangles.loc[j, i] = rect_id

    def update_memory(self, upd_list: Iterable):
        for index, value in upd_list:
            j, i = divmod(index, 8)
            rect_id = self.rectangles.loc[j, i]
            color = "gray" if value == "Allocated" else "sky blue"
            self.memory_canvas.itemconfig(rect_id, fill=color)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Visualization')
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))  # 按下Esc退出全屏
    app = Visualization(root)
    root.mainloop()
