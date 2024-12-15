import math
from process_control_block import PCB

class MainMemory:
    def __init__(self, real_page_num: int, page_size: int):
        self.real_page_num = real_page_num    # 实页（页框）数
        self.state = [False] * real_page_num  # 实页是否被占用
        self.page_size = page_size            # 一个页面的字节数
        self.PCBs = {}                        # 当前内存中的所有进程

    def allocate(self, pid: str, bytes: int) -> str | None:
        need_pages = math.ceil(bytes / self.page_size)
        if need_pages > self.real_page_num:
            return '内存不够分配'
        
        if pid not in self.PCBs:
            self.PCBs[pid] = PCB(pid=pid, bytes=bytes)

        pcb = self.PCBs[pid]
        cnt = 0
        for index, row in pcb.page_table.iterrows():
            if row['valid'] == True:
                continue

            # 分配实页
            pcb.page_table.loc[index, 'valid'] = True
            for i in range(len(self.state)):
                if self.state[i] == True:
                    continue
                self.state[i] = True
                pcb.page_table.loc[index, 'real_page_num'] = i
                break

            # 计数
            cnt += 1
            self.real_page_num -= 1
            if cnt == need_pages:
                break
    
    def free(self, pid: str) -> str | None:
        if pid not in self.PCBs:
            return '不存在当前进程'
        
        pcb = self.PCBs[pid]
        for _, row in pcb.page_table.iterrows():
            if row['valid'] is True:
                self.real_page_num += 1
                self.state[row['real_page_num']] = False
        del self.PCBs[pid]

    def show(self) -> None:
        print('作业名\t占用页面数\t占用页框号')
        for pid, pcb in self.PCBs.items():
            cnt = 0
            real_pages = []
            for _, row in pcb.page_table.iterrows():
                if row['valid'] is True:
                    cnt += 1
                    real_pages.append(row['real_page_num'])
            print(f'{pid}\t{cnt}\t{real_pages}')

    def get_real_page(self, pid: str, bytes_delta: int) -> str | int:
        pcb: PCB = self.PCBs[pid]
        if pcb.bytes < bytes_delta:
            return '越界！'
        
        virt_page = bytes_delta // self.page_size
        real_page = pcb.page_table.loc[virt_page, 'real_page_num']
        return real_page
