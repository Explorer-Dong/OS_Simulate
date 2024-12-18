import tkinter as tk
from typing import Iterable
import pandas as pd
from config import msg_queue
import queue


class Visualization(object):
    def __init__(self, master: tk.Tk, realPageNumber=64, pageSize=1000):
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
        self.page8pid = {}

        self.check_msgQueue()

    def init_page(self, pid: str):
        canvas_number = -1
        for i in range(6):
            if self.page8pid.get(i, -1) == -1:
                self.page8pid[i] = pid
                self.page8pid[pid] = i
                canvas_number = i
                break

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

    def update_page(self, pid: str, record_list: Iterable):
        canvas_number = self.page8pid[pid]
        id_list = self.id_dict[canvas_number]
        for i, record in enumerate(record_list):
            address = str(record) if record is not None else ""
            self.page_canvas[canvas_number].itemconfig(
                id_list[i], text=address,
            )

    def clear_page(self, pid: str):
        canvas_number = self.page8pid[pid]
        self.page_canvas[canvas_number].delete("all")
        self.id_dict[canvas_number] = []
        self.page8pid.pop(canvas_number)
        self.page8pid.pop(pid)

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

    def allocate_memory(self, index: int, pid: str):
        j, i = divmod(index, 8)
        rect_id = self.rectangles.loc[j, i]
        color = "gray"
        self.memory_canvas.itemconfig(rect_id, fill=color)

    def free_memory(self, index: int):
        j, i = divmod(index, 8)
        rect_id = self.rectangles.loc[j, i]
        color = "sky blue"
        self.memory_canvas.itemconfig(rect_id, fill=color)

    def solve_message(self, msg):
        """
        1. "Allocate", pid, page_number
        2. "Free", page_number
        3. "new_page", pid
        4. "update_page", pid, record_list
        5. "delete_page", pid
        """
        match msg[0]:
            case "Allocate":
                self.allocate_memory(msg[2], msg[1])
            case "Free":
                self.free_memory(msg[1])
            case "new_page":
                self.init_page(msg[1])
            case "update_page":
                self.update_page(msg[1], msg[2])
            case "delete_page":
                self.clear_page(msg[1])

    def check_msgQueue(self):
        try:
            while True:
                msg = msg_queue.get_nowait()
                print("Visualization get message: ", msg)
                self.solve_message(msg)
        except queue.Empty:
            pass
        self.master.after(100, self.check_msgQueue)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Visualization')
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))  # 按下Esc退出全屏
    app = Visualization(root)
    root.mainloop()
