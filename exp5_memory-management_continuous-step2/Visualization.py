import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Iterable
import pandas as pd

from main_memory import MainMemory
logging.basicConfig(level=logging.INFO)


class Visualization(object):
    def __init__(self, master, realPageNumber=100, pageSize=1000):
        self.realPageNumber = realPageNumber
        self.pageSize = pageSize
        self.mainMemory = MainMemory(realPageNumber, pageSize)
        self.master = master
        self.create_buttons()
        self.create_inputText()
        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.pack()
        self.rowMaxNumber = 10
        self.draw_memory()

    def draw_memory(self):
        self.canvas.delete("all")
        width, height = 20, 20
        n = self.rowMaxNumber
        self.rectangles = pd.DataFrame(
            index=range(self.realPageNumber // n),
            columns=range(n),
        )
        for k in range(self.realPageNumber):
            j, i = divmod(k, n)
            x = i * width + 300
            y = j * height + 50
            rect_id = self.canvas.create_rectangle(
                x, y, x + width, y + height, fill="sky blue",
            )
            self.rectangles.loc[j, i] = rect_id
            # self.canvas.itemconfig(rect_id, fill="sky blue")

    def update_memory(self, upd_list: Iterable):
        for index, value in upd_list:
            j, i = divmod(index, self.rowMaxNumber)
            rect_id = self.rectangles.loc[j, i]
            color = "gray" if value == "Allocated" else "sky blue"
            self.canvas.itemconfig(rect_id, fill=color)

    def create_inputText(self):
        frame = tk.Frame(self.master)
        frame.pack()

        tk.Label(frame, text="PID: ").pack(side='left')
        self.pidInput = tk.Entry(frame)
        self.pidInput.pack(side='left', padx=10, pady=10)

        tk.Label(frame, text="(Δ)Bytes: ").pack(side='left')
        self.bytesInput = tk.Entry(frame)
        self.bytesInput.pack(side='left', padx=10, pady=10)

    def create_buttons(self):
        frame = tk.Frame(self.master)
        frame.pack()

        names = ['Allocate', 'Free', 'Show', 'GetRealPage']
        operators = [self.allocate_button, self.free_button, self.show_button, self.getRealPage_button]
        for i, name, operator in zip(range(4), names, operators):
            button = ttk.Button(
                frame, text=name, command=operator,
            )
            button.pack(side='left', padx=10, pady=10)

    def allocate_button(self):
        logging.info("Allocate button clicked")
        pid = self.pidInput.get()
        bytes = int(self.bytesInput.get())
        state = self.mainMemory.allocate(pid, bytes)
        if type(state) is str:
            messagebox.showerror(title='Error', message=state)
        else:
            self.update_memory(state)

    def free_button(self):
        logging.info("Free button clicked")
        pid = self.pidInput.get()
        state = self.mainMemory.free(pid)
        if type(state) is str:
            messagebox.showerror(title='Error', message=state)
        else:
            self.update_memory(state)

    def show_button(self):
        logging.info("Show button clicked")
        msg = self.mainMemory.show()
        title = msg['title']
        message = msg['msg']
        window = tk.Toplevel(self.master)
        tree = ttk.Treeview(window, columns=title, show='headings')
        for i, col in enumerate(title):
            tree.heading(i, text=col)
            tree.column(i, anchor='center')

        for row in message:
            tree.insert('', 'end', values=row)
        # 设置滚动条
        scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        tree.pack()
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def getRealPage_button(self):
        logging.info("GetRealPage button clicked")
        pid = self.pidInput.get()
        bytes = int(self.bytesInput.get())
        result = self.mainMemory.get_real_page(pid, bytes)
        if type(result) is str:
            messagebox.showerror(title='Error', message=result)
        else:
            delta = bytes % self.pageSize
            real_address = str(result) + str(delta)
            logging.info(f"GetRealPage {pid}, {bytes}, real address: {real_address}")
            messagebox.showinfo(title='GetRealPage', message=f"Real address: {real_address}")


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Visualization')
    root.geometry('800x600')
    app = Visualization(root)
    root.mainloop()
