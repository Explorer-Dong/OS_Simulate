import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
        self.rowMaxNumber = 50
        self.draw_memory()

    def draw_memory(self):
        self.canvas.delete("all")
        width, height = 10, 10
        n = self.rowMaxNumber
        self.rectangles = pd.DataFrame(
            index=range(self.pageSize // n),
            columns=range(n),
        )
        for k in range(self.pageSize):
            j, i = divmod(k, n)
            x = i * width + 30
            y = j * height + 30
            rect_id = self.canvas.create_rectangle(
                x, y, x + width, y + height, fill="gray",
            )
            self.rectangles.loc[j, i] = rect_id
            # self.canvas.itemconfig(rect_id, fill="sky blue")

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

    def free_button(self):
        logging.info("Free button clicked")
        pid = self.pidInput.get()
        state = self.mainMemory.free(pid)
        if type(state) is str:
            messagebox.showerror(title='Error', message=state)

    def show_button(self):
        logging.info("Show button clicked")
        text = self.mainMemory.show()

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


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Visualization')
    root.geometry('800x600')
    app = Visualization(root)
    root.mainloop()
