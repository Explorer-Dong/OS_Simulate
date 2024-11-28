import threading
import numpy as np
import tkinter as tk
from tkinter import font


class Fork:
    def __init__(self, canvas, r, theta, width, offset, line_id=None):
        self.const_init = (r, theta, width, offset)
        self.canvas = canvas
        p = np.array([np.cos(theta), np.sin(theta)])
        self.p1 = p * (r + width) + offset
        self.p2 = p * (r - width) + offset
        self.line_id = line_id
        self.draw()

    def rotate(self, theta):
        r, t, w, o = self.const_init
        t += theta
        p = np.array([np.cos(t), np.sin(t)])
        self.p1 = p * (r + w) + o
        self.p2 = p * (r - w) + o
        self.draw()

    def restore(self):
        self.__init__(self.canvas, *self.const_init, line_id=self.line_id)

    def draw(self):
        if self.line_id is not None:
            self.canvas.delete(self.line_id)
        self.line_id = self.canvas.create_line(
            *self.p1, *self.p2, fill="black", width=4
        )


class Philosopher:
    def __init__(self, canvas, r, theta, size, offset):
        self.canvas = canvas
        self.text_id = None
        self.circle_id = None
        p = np.array([np.cos(theta), np.sin(theta)])
        self.p1 = p * r + np.array([size, size]) + offset
        self.p2 = p * r + np.array([-size, -size]) + offset
        self.state = "thinking"
        self.color = "blue"
        self.draw()

    def draw(self):
        if self.text_id is not None:
            self.canvas.delete(self.text_id)
        if self.circle_id is not None:
            self.canvas.delete(self.circle_id)
        self.circle_id = self.canvas.create_oval(
            *self.p1, *self.p2, fill=self.color
        )
        self.text_id = self.canvas.create_text(
            *((self.p1 + self.p2) / 2),
            text=self.state, fill="black", font=font.Font(
                family="Cursive", size=15, slant="italic"
            )
        )

    def state_change(self, new_state):
        if self.state == new_state:
            return
        self.state = new_state
        if self.state == "thinking":
            self.color = "blue"
        elif self.state == "hungry":
            self.color = "red"
        elif self.state == "eating":
            self.color = "green"
        self.draw()


class Visualizer:
    def __init__(
            self, master=None,
            num=5, radius=100,
            philosopher_radius=5, fork_width=10
    ):
        self.num = num
        self.radius = radius
        theta = 2 * np.pi / num
        self.philosopher_radius = philosopher_radius
        self.fork_width = fork_width

        self.offset = self.radius // 2
        self.canvas = tk.Canvas(
            master,
            width=(self.radius + self.offset) * 2,
            height=(self.radius + self.offset) * 2
        )
        self.canvas.pack()

        self.canvas.create_oval(
            self.offset, self.offset,
            self.radius * 2 + self.offset, self.radius * 2 + self.offset,
            fill="white"
        )

        self.offset += self.radius

        self.philosophers = [
            Philosopher(
                canvas=self.canvas,
                r=radius, theta=theta * i,
                size=philosopher_radius, offset=self.offset
            )
            for i in range(num)
        ]

        self.forks = [
            Fork(
                canvas=self.canvas,
                r=radius, theta=theta * i + theta / 2,
                width=fork_width, offset=self.offset
            )
            for i in range(num)
        ]

        self.canvas.update()

    def get_fork(self, philosopher_id, fork_id):
        theta = 2 * np.pi / self.num
        philosopher = self.philosophers[philosopher_id]
        fork = self.forks[fork_id]

        if philosopher_id == fork_id:
            fork.rotate(-theta / 2)
        else:
            fork.rotate(theta / 2)

    def put_fork(self, philosopher_id, fork_id):
        philosopher = self.philosophers[philosopher_id]
        fork = self.forks[fork_id]
        fork.restore()

    def change_state(self, philosopher_id, state):
        self.philosophers[philosopher_id].state_change(state)


def main():
    root = tk.Tk()
    num_philosophers = 5
    radius = 200
    philosopher_radius = 15
    fork_width = 20
    root.title("Queue Visualizer")
    frame = tk.Frame(root)
    frame.pack()
    app = Visualizer(frame, num_philosophers, radius, philosopher_radius, fork_width)
    root.mainloop()


if __name__ == "__main__":
    main()
