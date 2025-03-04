from process import Process
from config import *
import tkinter as tk
from Visualization import Visualization


if __name__ == '__main__':
    # 所有进程开始运行
    processes = []
    threads = []
    for i in range(process_num):
        pid = f'pro {i}'

        pro = Process(pid, access_num=access_num, algo='lru' if i % 2 == 1 else 'fifo')
        processes.append(pro)
        
        thread = threading.Thread(target=pro.run)
        threads.append(thread)
        thread.start()

    # 启动可视化
    root = tk.Tk()
    root.title('Visualization')
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', lambda e: root.attributes('-fullscreen', False))  # 按下Esc退出全屏
    app = Visualization(root)
    root.mainloop()

    # 等所有进程结束后输出每一个进程的缺页中断率
    for thread in threads:
        thread.join()
    for process in processes:
        print(f"{process.pid} 的缺页率为 {process.info()['fail_cnt'] / access_num}")
