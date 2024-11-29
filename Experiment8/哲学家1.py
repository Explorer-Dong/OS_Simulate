from threading import Thread, Semaphore
import time
from Visualizer import Visualizer
import tkinter as tk

room = Semaphore(4)
fork = [Semaphore(1) for i in range(5)]


# 哲学家类
class Philosopher(object):
    def __init__(
            self, name, left_fork, right_fork,
            left_neighbour, right_neighbour,
            visualizer
    ):
        """
        :param name: 哲学家编号
        :param left_fork: 左筷子编号
        :param right_fork: 右筷子编号
        :param visualizer: 可视化器
        """
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.state = "thinking"
        self.visualizer = visualizer
        self.left_neighbour = left_neighbour
        self.right_neighbour = right_neighbour

    def think(self):
        """ 思考 """
        self.state = "thinking"
        self.visualizer.change_state(self.name, self.state)
        time.sleep(1)

    def eat(self):
        """ 吃 """
        self.state = "eating"
        self.visualizer.change_state(self.name, self.state)
        time.sleep(1)

    def hungry(self):
        """ 饥饿 """
        self.state = "hungry"
        self.visualizer.change_state(self.name, self.state)
        time.sleep(1)

    def take_fork(self):
        self.hungry()
        fork[self.left_fork].acquire()
        fork[self.right_fork].acquire()
        self.visualizer.get_fork(self.name, self.left_fork)
        self.visualizer.get_fork(self.name, self.right_fork)
        self.eat()

    def put_fork(self):
        fork[self.left_fork].release()
        fork[self.right_fork].release()
        self.visualizer.put_fork(self.name, self.left_fork)
        self.visualizer.put_fork(self.name, self.right_fork)
        self.think()

    def run(self):
        while True:
            self.think()
            room.acquire()
            self.take_fork()
            self.put_fork()
            room.release()


def main():
    root = tk.Tk()
    num_philosophers = 5
    radius = 200
    philosopher_radius = 15
    fork_width = 20
    root.title("Queue Visualizer")
    frame = tk.Frame(root)
    frame.pack()
    visualizer = Visualizer(frame, num_philosophers, radius, philosopher_radius, fork_width)

    philosophers = [
        Philosopher(
            i, (i - 1) % 5, i,
            None, None, visualizer
        )
        for i in range(5)
    ]
    for i in range(5):
        philosophers[i].left_neighbour = philosophers[(i - 1) % 5]
        philosophers[i].right_neighbour = philosophers[(i + 1) % 5]

    threads = [Thread(target=philosopher.run) for philosopher in philosophers]
    for thread in threads:
        thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
