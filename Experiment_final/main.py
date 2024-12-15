from page_replacement_algorithm import FIFO, LRU
from memory_manager import MemoryManager, P, V
from process import Process
import time

import threading

# 互斥信号量，同时只能有一个进程申请内存
mutex = threading.Semaphore(1)

# 最大进程数
num_process = 12

# 进程运行开关
running = True

memory_manager: MemoryManager = None

fifo_algorithm = lru_algorithm = None


def process_thread(i):
    time.sleep(1)
    while running:
        # 申请内存
        P(mutex)
        allocated_pages = memory_manager.allocate_memory(num_pages = 10)
        V(mutex)

        # 申请不到时跳过
        if allocated_pages is None:
            continue

        fifo_algorithm = FIFO(9)
        lru_algorithm = LRU(9)
        
        # 申请到内存后，开始执行进程
        process = Process(i, memory_manager, lru_algorithm, allocated_pages)
        process.run()

        # 释放内存
        P(mutex)
        memory_manager.deallocate_memory(allocated_pages)
        V(mutex)
        input()

def main():
    global memory_manager

    total_memory_size = 2 ** 14
    page_size = 256
    num_pages = total_memory_size // page_size
    memory_manager = MemoryManager(total_memory_size, page_size, num_pages)

    

    processes = [threading.Thread(target = process_thread, args = (i,)) for i in range(num_process)]
    for process in processes:
        process.start()

if __name__ == "__main__":
    main()
