import threading

real_page_num = 64              # 实页（页框）数
virt_page_num = 64              # 虚页（页）数
page_size = 256                 # 页面大小（字节）
allocate_per_process = 10       # 每个进程分配的实页数
process_num = 12                # 并发进程数
mutex = threading.Semaphore(1)  # 内存访问锁
