from config import *

class MainMemory:
    def __init__(self):
        self.remain_real_page_num = real_page_num  # 剩余实页的数量
        self.state = [False] * real_page_num       # 实页是否被占用

    def allocate(self, need_page_num: int, pro) -> bool:
        # 内存不够分配
        if need_page_num > self.remain_real_page_num:
            return False
        
        cnt = 0
        for index, row in pro.page_table.iterrows():
            if row['valid']:
                continue

            # 分配实页
            pro.page_table.loc[index, 'valid'] = True
            for i in range(len(self.state)):
                if self.state[i]:
                    continue
                self.state[i] = True
                pro.page_table.loc[index, 'real_page_id'] = i
                break

            # 计数
            cnt += 1
            self.remain_real_page_num -= 1
            if cnt == need_page_num:
                break
        return True

    def free(self, pro) -> None:
        for _, row in pro.page_table.iterrows():
            if row['valid']:
                self.remain_real_page_num += 1
                real_page_id = row['real_page_id']
                self.state[real_page_id] = False

    # def get_real_page(self, pid: str, bytes_delta: int) -> str | int:
    #     pcb: PCB = self.PCBs[pid]
    #     if pcb.bytes < bytes_delta:
    #         return '越界！'
    #
    #     virt_page = bytes_delta // page_size
    #     real_page = pcb.page_table.loc[virt_page, 'real_page_num']
    #     return real_page

main_mem = MainMemory()
