from process import Process
from config import *

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
    
    # 等所有进程结束后输出每一个进程的缺页中断率
    for thread in threads:
        thread.join()
    for process in processes:
        print(process.info())
