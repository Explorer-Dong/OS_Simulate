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

        pro = Process(pid, access_num=3, algo='lru' if i % 2 == 1 else 'fifo')
        processes.append(pro)
        
        thread = threading.Thread(target=pro.run)
        threads.append(thread)
        thread.start()

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
        print(process.info())

    # import pandas as pd
    # while msg_queue.empty() is False:
    #     msg = msg_queue.get()
    #     if msg[0] == 'update_page':
    #         task_name = msg[1]
    #         df: pd.DataFrame = msg[2]
    #         for i in range(64):
    #             if df.iloc[i]['valid']:
    #                 print(df.iloc[i]['real_page_id'], end=' ')
    #         print('\n\n')
    #     else:
    #         print(msg)
