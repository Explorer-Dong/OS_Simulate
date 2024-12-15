import threading

def P(semaphore: threading.Semaphore):
    semaphore.acquire()

def V(semaphore: threading.Semaphore):
    semaphore.release()

class MemoryManager:
    def __init__(self, total_memory_size, page_size, num_pages):
        self.total_memory_size = total_memory_size
        self.page_size = page_size
        self.num_pages = num_pages
        self.free_pages = num_pages
        self.memory = [None] * total_memory_size
    

        # 从data.txt中读取数据，存入一个字典内
        self.folder_data = {}
        self.init_data()
        
        # self.processes = []

        self.bitmap = [0] * num_pages
        self.cnt_access_memory = 0  # 访问内存次数
        self.cnt_page_fault = 0  # 缺页次数


    def init_data(self):
        with open("data.txt", "r") as file:
            for line in file:
                line = line.strip()
                line = line.split(" ")
                self.folder_data[(int(line[0]), int(line[1]))] = int(line[2])
        
    def allocate_memory(self, num_pages):
        if self.free_pages < num_pages:
            return None  
        cur = 0
        while cur < self.num_pages:
            if self.bitmap[cur] == 0:
                self.bitmap[cur] = 1
                break
            cur += 1
        self.free_pages -= 1
        page_table = {'base': cur,
                      'page': [None] * 64,
                      'data': []}
        for i in range(num_pages-1):
            while self.bitmap[cur] == 1:
                cur = (cur + 1) % self.num_pages
            self.bitmap[cur] = 1
            page_table["data"].append(cur)
            self.free_pages -= 1
        return page_table


    def deallocate_memory(self, pages):
        self.bitmap[pages['base']] = 0
        self.free_pages += 1
        for page in pages["data"]:
            self.bitmap[page] = 0
            self.free_pages += 1