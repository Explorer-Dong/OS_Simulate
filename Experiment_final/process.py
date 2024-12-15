from memory_manager import MemoryManager
from page_replacement_algorithm import PageReplacementAlgorithm
import time
import random
import math

# 每个进程随机生成200次逻辑地址
num_random_logical_addresses = 200
x = [i for i in range(64)]
p = [1 / math.sqrt(i + 1) for i in range(64)]


def number_of_certain_probability(sequence, probability):
    x = random.uniform(0, sum(p))
    cumulative_probability = 0.0
    for item, item_probability in zip(sequence, probability):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


class Process:
    def __init__(self, process_id: int, memory_manager: MemoryManager, page_algorithm: PageReplacementAlgorithm,
                 allocated_pages):
        """
        初始化进程对象
        :param process_id: 进程id
        :param memory_manager: 内存管理器参数
        :param page_algorithm: 替换页面算法
        :param page_table: 页表, 个页表项占4个字节(系统的物理页面数为2 ** 6,每个页表正好占一个页面)
        :param cnt_page_faults: 缺页次数
        """
        self.process_id = process_id
        self.memory_manager: MemoryManager = memory_manager
        self.page_algorithm: PageReplacementAlgorithm = page_algorithm
        self.page_table = allocated_pages
        self.cnt_page_faults = 0

    def run(self):
        print(f"进程 {self.process_id} 启动.")
        for _ in range(num_random_logical_addresses):
            logical_address = self.generate_logical_address()
            self.access_memory(_, logical_address)
            sleep_time = self.generate_sleep_time()
            time.sleep(sleep_time)
        print(f"进程 {self.process_id} 结束执行. Page faults: {self.cnt_page_faults}")
        print(f"进程 {self.process_id} 缺页中断率：{self.cnt_page_faults / num_random_logical_addresses}")

    @staticmethod
    def generate_logical_address():
        offset = random.randint(0, 2 ** 8 - 1)
        page = number_of_certain_probability(x, p)
        address = (page << 8) + offset
        # print(hex(address))

        return address

    @staticmethod
    def generate_sleep_time():
        """
        每次地址访问后休眠（0-100ms)中的一个随机值
        :rtype: 每个进程的访存时间为 0 - 100ms
        """
        return random.randint(0, 100) / 1000.0

    def access_memory(self, idx: int, logical_address: int):
        """
        访问内存
        :param logical_address:逻辑地址
        """
        # 访问的页数 = 逻辑地址 // 页面大小
        page_number = logical_address // self.memory_manager.page_size

        self.memory_manager.cnt_access_memory += 1

        val = 0
        if self.page_table['page'][page_number] is None:
            self.cnt_page_faults += 1
            # print("缺页")
            self.memory_manager.cnt_page_fault += 1
            val = self.memory_manager.folder_data[(self.process_id, page_number)]

        self.page_algorithm.replace_page(self.memory_manager.memory, page_number, self.page_table, val)

        offset = logical_address % self.memory_manager.page_size

        if idx % 50 == 0:
            print(self.process_id, "逻辑地址", hex(logical_address),
                  "页面内容", self.page_table,
                  "物理地址", hex(self.page_table['page'][page_number] * self.memory_manager.page_size + offset),
                  "物理地址内容", val)
