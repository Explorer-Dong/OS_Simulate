import time
import tkinter as tk
from tkinter import ttk
from typing import Iterable
import pandas as pd
from config import msg_queue
import queue


class Visualization(object):
    def __init__(self, master: tk.Tk, realPageNumber=64, pageSize=1000):
        self.realPageNumber = realPageNumber
        self.pageSize = pageSize
        self.master = master

        top_frame = tk.Frame(self.master)
        top_frame.pack(side=tk.TOP)
        self.memory_canvas = tk.Canvas(top_frame, width=400, height=400)
        self.memory_canvas.pack(side=tk.LEFT)
        self.draw_memory()

        button_frame = tk.Frame(top_frame)
        button_frame.pack(side=tk.LEFT)
        ttk.Button(
            button_frame, text="start",
            command=self.start_simulation
        ).pack(side=tk.TOP)

        ttk.Button(
            button_frame, text="pause",
            command=self.pause_simulation
        ).pack(side=tk.TOP)

        canvas = tk.Canvas(self.master, width=100, height=400)
        canvas.pack()
        self.page_canvas = [
            tk.Canvas(canvas, width=150, height=400, bg="white")
            for i in range(6)
        ]
        [c.pack(side=tk.LEFT, padx=10, pady=5) for c in self.page_canvas]
        self.id_dict = {}
        self.page8pid = {}

        self.running = False


    def init_page(self, pid: str, replace_algorithm: str):
        canvas_number = -1
        for i in range(6):
            if self.page8pid.get(i, -1) == -1:
                self.page8pid[i] = pid
                self.page8pid[pid] = i
                canvas_number = i
                break

        canvas = self.page_canvas[canvas_number]
        canvas.create_text(
            70, 20,
            text=pid,
            font=("Arial", 15),
        )
        canvas.create_text(
            70, 60,
            text=replace_algorithm,
            font=("Arial", 15),
        )
        canvas.create_rectangle(
            20, 80, 130, 400,
        )
        canvas.create_line(
            75, 80, 75, 400
        )
        height = 35
        id_list = []
        for i in range(9):
            canvas.create_line(
                20, 80 + i * height,
                130, 80 + i * height,
            )
            text_id1 = canvas.create_text(
                45, 80 + height // 2 + i * height,
                text="",
                font=("Arial", 10),
            )
            text_id2 = canvas.create_text(
                100, 80 + height // 2 + i * height,
                text="",
                font=("Arial", 10),
            )
            id_list.append([text_id1, text_id2])
        self.id_dict[canvas_number] = id_list

    def update_page(self, pid: str, page_table: pd.DataFrame):
        canvas_number = self.page8pid[pid]
        id_list = self.id_dict[canvas_number]
        cnt = 0
        for virtual_id, row in page_table.iterrows():
            if row['valid'] == True:
                real_id = row['real_page_id']

                self.page_canvas[canvas_number].itemconfig(
                    id_list[cnt][0], text=str(virtual_id),
                )
                self.page_canvas[canvas_number].itemconfig(
                    id_list[cnt][1], text=str(real_id),
                )

                cnt += 1

    def clear_page(self, pid: str):
        canvas_number = self.page8pid[pid]
        self.page_canvas[canvas_number].delete("all")
        self.id_dict[canvas_number] = []
        self.page8pid.pop(canvas_number)
        self.page8pid.pop(pid)

    def draw_memory(self):
        self.memory_canvas.delete("all")
        width, height = 40, 40
        self.rectangles = pd.DataFrame(
            index=range(8),
            columns=range(8),
        )
        self.memory_text = pd.DataFrame(
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
            text_id = self.memory_canvas.create_text(
                x + width // 2, y + height // 2,
                text="",
                font=("Arial", 10),
            )
            self.rectangles.loc[j, i] = rect_id
            self.memory_text.loc[j, i] = text_id

    def allocate_memory(self, index: int, pid: str):
        j, i = divmod(index, 8)
        rect_id = self.rectangles.loc[j, i]
        text_id = self.memory_text.loc[j, i]
        color = "gray"
        self.memory_canvas.itemconfig(rect_id, fill=color)
        self.memory_canvas.itemconfig(text_id, text=pid)

    def free_memory(self, index: int):
        j, i = divmod(index, 8)
        rect_id = self.rectangles.loc[j, i]
        text_id = self.memory_text.loc[j, i]
        color = "sky blue"
        self.memory_canvas.itemconfig(rect_id, fill=color)
        self.memory_canvas.itemconfig(text_id, text="")

    def solve_message(self, msg):
        """
        1. "allocate_memory", page_number, pid
        2. "free_memory", page_number
        3. "new_page", pid
        4. "update_page", pid, page_table
        5. "delete_page", pid
        """
        match msg[0]:
            case "allocate_memory":
                self.allocate_memory(msg[1], msg[2])
            case "free_memory":
                self.free_memory(msg[1])
            case "new_page":
                self.init_page(msg[1], msg[2])
            case "update_page":
                self.update_page(msg[1], msg[2])
            case "delete_page":
                self.clear_page(msg[1])

    def check_msgQueue(self):
        if not self.running:
            return
        try:
            msg = msg_queue.get_nowait()
            self.solve_message(msg)
            self.master.after(200, self.check_msgQueue)
        except queue.Empty:
            self.master.after(100, self.check_msgQueue)

    def start_simulation(self):
        self.running = True
        self.check_msgQueue()

    def pause_simulation(self):
        self.running = False


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Visualization')
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))  # 按下Esc退出全屏
    app = Visualization(root)
    root.mainloop()
