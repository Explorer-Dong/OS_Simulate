import random
from threading import Semaphore, Thread
import tkinter as tk
import logging
from time import sleep

mutex = Semaphore(1)  # 互斥锁
s2 = Semaphore(10)  # 空位
s3 = Semaphore(0)  # 产品
stop_signal = False  # 停止信号


class QueueVisualizer:
    def __init__(self, master, max_size=10):
        self.master = master
        self.max_size = max_size
        self.shop = ["None" for _ in range(max_size)]
        self.put_idx = 0
        self.get_idx = 0

        # 设置画布
        self.width, self.height = 1000, 400
        self.canvas = tk.Canvas(
            self.master, width=self.width, height=self.height, bg="white"
        )
        self.canvas.pack()

        # 初始化格子
        self.draw_boxes()
        button_frame = tk.Frame(self.master)
        button_frame.pack(side="bottom", pady=20)
        # 启动按钮
        self.start_button = tk.Button(
            button_frame, text="Start", command=self.start,
            width=20, height=2, font=("Comic Sans MS", 16),
        )
        self.start_button.pack(side="left", padx=10, pady=10)

        # 结束按钮
        self.stop_button = tk.Button(
            button_frame, text="Stop", command=self.stop,
            width=20, height=2, font=("Comic Sans MS", 16),
        )
        self.stop_button.pack(side="left", padx=10, pady=10)

    def draw_boxes(self):
        """画5个格子，并根据队列的状态进行高亮显示"""
        width, height = 160, 160
        dx = self.width // 10
        dy = 50
        for i, item in enumerate(self.shop):
            color = "yellow" if item != "None" else "white"
            x = i % 5
            y = i // 5
            rect = self.canvas.create_rectangle(
                dx + x * width, dy + y * height,
                dx + (x + 1) * width, dy + (y + 1) * height,
                fill=color, outline="black",
                tags=f"box_{i}",
            )
            # 在每个格子里写上队列中的 item
            self.canvas.create_text(
                dx + x * width + width // 2,
                dy + y * height + height // 2,
                text=item, tags=f"text_{i}", font=("Comic Sans MS", 20),
            )

    def update_boxes(self):
        """根据队列当前状态更新格子的颜色和内容"""
        for i, item in enumerate(self.shop):
            color = "yellow" if item != "None" else "white"
            self.canvas.itemconfig(f"box_{i}", fill=color)
            self.canvas.itemconfig(f"text_{i}", text=item)
        self.canvas.update()

    def search_empty_slot(self, start=0, cmp=True):
        """查找空位，cmp=True 查找空位，cmp=False 查找产品"""
        # print(self.shop[start], self.shop[start % self.max_size] == "None" == cmp)
        while start < 2 * self.max_size:
            if (self.shop[start % self.max_size] == "None") == cmp:
                return start % self.max_size
            start += 1
        return None

    def put(self, obj):
        """将元素放入队列，并更新格子的状态"""
        if self.put_idx is None:
            self.put_idx = self.search_empty_slot()
        self.shop[self.put_idx] = obj
        self.update_boxes()
        self.put_idx = self.search_empty_slot(start=self.put_idx + 1)

    def get(self):
        """从队列中获取元素，并更新格子的状态"""
        if self.get_idx is None:
            self.get_idx = self.search_empty_slot(cmp=False)

        obj = self.shop[self.get_idx]
        self.shop[self.get_idx] = "None"
        self.update_boxes()

        self.get_idx = self.search_empty_slot(start=self.get_idx + 1, cmp=False)
        return obj

    def start(self):
        global stop_signal
        stop_signal = False
        for i in range(3):
            Thread(target=producer, args=(i,)).start()
        for i in range(2):
            Thread(target=consumer, args=(i,)).start()

    def stop(self):
        global stop_signal
        stop_signal = True
        logging.info("All threads have been released")


# 创建 Tkinter 主窗口
root = tk.Tk()
root.title("队列操作可视化")

# 创建队列可视化对象
q = QueueVisualizer(root)


def producer(Pno):
    while not stop_signal:
        production = random.choice(['apple', 'banana', 'cherry'])  # 随机生产产品
        s2.acquire()
        mutex.acquire()
        q.put(production)  # 放入产品
        logging.info(f"Producer {Pno} has put {production} into the queue")
        sleep(0.2)  # 随机等待时间
        mutex.release()
        s3.release()


def consumer(Cno):
    while not stop_signal:
        s3.acquire()
        mutex.acquire()
        production = q.get()
        logging.info(f"Consumer {Cno} has taken {production} from the queue")
        sleep(0.3)  # 随机等待时间
        mutex.release()
        s2.release()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # 启动 Tkinter 事件循环
    root.mainloop()
