from config import *
from main_memory import main_mem
import pandas as pd

class Process:
    def __init__(self, pid: str):
        self.pid = pid
        self.page_table = pd.DataFrame({
            'valid': [False] * virt_page_num,       # 有效位
            'real_page_id': [None] * virt_page_num  # 实页页号
        })
    
    def run(self) -> None:
        while True:
            ok = self.__acquire_page()
            if ok:
                self.__execute()
                self.__release_page()
                break
    
    def info(self) -> str:
        return self.pid + ' info'
    
    def __acquire_page(self) -> bool:
        mutex.acquire()
        allocate_cond = main_mem.allocate(
            need_page_num=allocate_per_process,pro=self)
        mutex.release()
        return allocate_cond
    
    def __execute(self) -> None:
        # 命中内存单元 TODO
        print('命中内存单元')
        
        # 未命中内存单元 TODO
        print('执行缺页中断')
    
    def __release_page(self) -> None:
        mutex.acquire()
        main_mem.free(pro=self)
        mutex.release()
