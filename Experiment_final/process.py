from config import *
from main_memory import main_mem
import pandas as pd
import numpy as np
import time
from collections import deque

def gen_virt_page_id(data_range: int, sample_num: int) -> list[int]:
    """ 生成 sample_num 个数据，每一个数据的取值范围为 [0,data_range) """
    weights = np.array([1 / np.sqrt(i + 2) for i in range(data_range)])
    weights /= weights.sum()  # 归一化
    virt_page_id = np.random.choice(range(data_range), size=sample_num, p=weights)
    return virt_page_id.tolist()


class Process:
    def __init__(self, pid: str, access_num: int=200, algo: str='lru'):
        self.pid = pid
        self.page_replace_algo = algo                      # 进程的页面替换算法
        self.access_num = access_num                       # 每一个进程访问内存的次数
        self.access_info = {'fail_cnt': 0, 'details': []}  # 访问情况
        self.page_table_id = None                          # 进程页表地址
        self.valid_virt_page_queue = deque()               # 已分配实页的虚页队列
        self.page_table = pd.DataFrame({                   # 进程页表
            'valid': [False] * virt_page_num,
            'real_page_id': [None] * virt_page_num
        })
    
    def run(self) -> None:
        while True:
            ok = self.__acquire_page()
            if ok:
                self.__execute()
                self.__release_page()
                break
    
    def info(self) -> dict:
        return self.access_info
    
    def __acquire_page(self) -> bool:
        mutex.acquire()
        allocate_cond = main_mem.allocate(
            need_page_num=allocate_per_process,pro=self)
        mutex.release()
        return allocate_cond
    
    def __execute(self) -> None:
        # 生成 200 条逻辑地址（此处只生成虚页号，页内偏移省略）
        virt_page_ids = gen_virt_page_id(virt_page_num, self.access_num)
        
        # 内存访问
        for virt_page_id in virt_page_ids:
            real_page_id = self.__access_main_mem(virt_page_id)
            self.access_info['details'].append((self.pid, virt_page_id, real_page_id))
            time.sleep(np.random.uniform(0, 0.1))
    
    def __release_page(self) -> None:
        mutex.acquire()
        main_mem.free(pro=self)
        mutex.release()
    
    def __access_main_mem(self, virt_page_id: int) -> int:
        # 命中内存，直接返回
        if self.page_table.loc[virt_page_id, 'valid']:
            if self.page_replace_algo == 'lru':
                self.__LRU(virt_page_id)  # 更新 LRU 队列
            return self.page_table.loc[virt_page_id, 'real_page_id']
        
        # 缺页中断，更新页表
        self.access_info['fail_cnt'] += 1
        if self.page_replace_algo == 'lru':
            self.__LRU(virt_page_id)
        elif self.page_replace_algo == 'fifo':
            self.__FIFO(virt_page_id)
        else:
            raise ValueError(f'页面替换算法 {self.page_replace_algo} 未定义！')
        
        return self.page_table.loc[virt_page_id, 'real_page_id']
    
    def __LRU(self, new_virt_page_id: int) -> None:
        # 若本就存在，更新队列顺序即可，无需改页表
        if new_virt_page_id in self.valid_virt_page_queue:
            self.valid_virt_page_queue.remove(new_virt_page_id)
            self.valid_virt_page_queue.append(new_virt_page_id)
            return
        
        # 若不存在，不但要更新队列，还需要改页表
        self.__FIFO(new_virt_page_id)
    
    def __FIFO(self, new_virt_page_id: int) -> None:
        # 修改已分配实页的虚页队列
        removed_virt_page_id = self.valid_virt_page_queue.popleft()
        self.valid_virt_page_queue.append(new_virt_page_id)
        
        # 更新页表
        self.page_table.loc[removed_virt_page_id, 'valid'] = False
        self.page_table.loc[new_virt_page_id, 'valid'] = True
        real_page_id = self.page_table.loc[removed_virt_page_id, 'real_page_id']
        self.page_table.loc[removed_virt_page_id, 'real_page_id'] = None
        self.page_table.loc[new_virt_page_id, 'real_page_id'] = real_page_id
