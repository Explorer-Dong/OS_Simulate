import tkinter as tk
from tkinter import ttk
from best_fit import BestFit
from first_fit import FirstFit
from worst_fit import WorstFit
from next_fit import NextFit

font = ("Arial", 12)


class UI:
    def __init__(self, master):
        self.algorithm_class: FirstFit | BestFit | WorstFit | NextFit | None = None

        self.master = master
        self.master.title("Experiment 10")
        self.master.geometry("800x700")
        self.max_length = 512

        self.generate_algorithm_choice()

        self.canvas = tk.Canvas(self.master, width=400, height=550, bg="white")
        self.canvas.pack(pady=10)
        self.x, self.y = 110, 15
        self.lx, self.ly = 200, 512

        self.space_init()
        self.generate_input_content()

    def insert(self, event=None):
        task_name = self.insert_name.get()
        task_size = int(self.insert_size.get())
        if task_name == "" or task_size == "":
            return
        self.algorithm_class.allocate(task_size, task_name)
        self.draw()

    def free(self, event=None):
        task_name = self.delete_name.get()
        if task_name == "":
            return
        self.algorithm_class.free(task_name)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        List = self.algorithm_class.tolist()
        print('\n')
        for start, Size, Name, status in List:
            print(start, Size, Name, status)
            color = "red" if status == "Allocated" else "green"
            size = int(Size / self.max_length * self.ly)
            self.canvas.create_rectangle(
                self.x, self.y + start,
                self.x + self.lx, self.y + start + size,
                fill=color, width=0
            )
            name = f"{Name} ({Size})" if status == "Allocated" else Size.__str__()
            self.canvas.create_text(
                self.x + self.lx / 2, self.y + start + size / 2,
                text=name, font=font
            )

    def space_init(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(self.x, self.y, self.x + self.lx, self.y + self.ly, fill="green")
        self.canvas.create_text(self.x + self.lx / 2, self.y + self.ly / 2, text=f"{self.max_length}", font=font)

    def generate_insert_content(self):
        frame = tk.Frame(self.master)
        frame.pack()

        label_name = tk.Label(frame, text="名称")
        label_name.pack(side=tk.LEFT, padx=5)

        entry_name = tk.Entry(frame)
        entry_name.pack(side=tk.LEFT, padx=5)

        label_size = tk.Label(frame, text="大小")
        label_size.pack(side=tk.LEFT, padx=5)

        entry_size = tk.Entry(frame)
        entry_size.pack(side=tk.LEFT, padx=5)

        button_insert = tk.Button(frame, text="插入", command=self.insert)
        button_insert.pack(side=tk.LEFT, padx=5)

        self.insert_name = entry_name
        self.insert_size = entry_size

    def generate_delete_content(self):
        frame = tk.Frame(self.master)
        frame.pack()

        label_name = tk.Label(frame, text="名称")
        label_name.pack(side=tk.LEFT, padx=5)

        entry_name = tk.Entry(frame)
        entry_name.pack(side=tk.LEFT, padx=5)

        button_delete = tk.Button(frame, text="删除", command=self.free)
        button_delete.pack(side=tk.LEFT, padx=5)

        self.delete_name = entry_name

    def generate_input_content(self):
        self.generate_insert_content()
        self.generate_delete_content()

    def generate_algorithm_choice(self):
        frame = tk.Frame(self.master)
        frame.pack()

        label_algorithm = tk.Label(frame, text="算法")
        label_algorithm.pack(side=tk.LEFT, padx=5)

        algorithm_choices = ["选择算法", "First", "Best", "Next", "Worst"]
        self.algorithm_choice = ttk.Combobox(
            frame, values=algorithm_choices, state="readonly",
        )
        self.algorithm_choice.pack(side=tk.LEFT, padx=5)
        self.algorithm_choice.bind("<<ComboboxSelected>>", self.algorithm_selected)

    def algorithm_selected(self, event):
        algorithm_choice = self.algorithm_choice.get()
        if algorithm_choice == "选择算法":
            self.algorithm_class = None
        elif algorithm_choice == "First":
            self.algorithm_class = FirstFit(maxLength=self.max_length)
        elif algorithm_choice == "Best":
            self.algorithm_class = BestFit(maxLength=self.max_length)
        elif algorithm_choice == "Next":
            self.algorithm_class = NextFit(maxLength=self.max_length)
        elif algorithm_choice == "Worst":
            self.algorithm_class = WorstFit(maxLength=self.max_length)
        else:
            return
        self.space_init()


if __name__ == "__main__":
    root = tk.Tk()
    ui = UI(root)
    root.mainloop()
