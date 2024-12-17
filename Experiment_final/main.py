from process import Process
import threading
from config import *

if __name__ == '__main__':
    # 所有进程开始运行
    processes = []
    threads = []
    for i in range(process_num):
        pid = f'pro {i + 1}'

        pro = Process(pid)
        processes.append(pro)
        
        thread = threading.Thread(target=pro.run)
        threads.append(thread)
        thread.start()
    
    # 等所有进程结束后输出每一个进程的缺页中断率
    for thread in threads:
        thread.join()
    for process in processes:
        print(process.info())
