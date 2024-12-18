from config import *


class MainMemory:
    def __init__(self):
        self.remain_real_page_num = real_page_num  # 剩余实页的数量
        self.state = [False] * real_page_num  # 实页是否被占用

    def allocate(self, need_page_num: int, pro) -> bool:
        # 内存不够分配
        if need_page_num > self.remain_real_page_num:
            return False

        # 分配页表
        for i in range(len(self.state)):
            if self.state[i]:
                continue
            self.state[i] = True
            self.remain_real_page_num -= 1
            pro.page_table_id = i
            msg_queue.put(
                ("allocate_memory", i, pro.pid)
            )
            break

        # 分配实页
        cnt = 0
        for virt_page_id, row in pro.page_table.iterrows():
            if row['valid']:
                continue

            pro.page_table.loc[virt_page_id, 'valid'] = True
            for i in range(len(self.state)):
                if self.state[i]:
                    continue
                self.state[i] = True
                msg_queue.put(
                    ("allocate_memory", i, pro.pid)
                )
                pro.page_table.loc[virt_page_id, 'real_page_id'] = i
                pro.valid_virt_page_queue.append(virt_page_id)
                break

            cnt += 1
            self.remain_real_page_num -= 1
            if cnt == need_page_num - 1:
                break
        return True

    def free(self, pro) -> None:
        # 释放页表
        self.remain_real_page_num += 1
        real_page_id = pro.page_table_id
        self.state[real_page_id] = False
        msg_queue.put(
            ("free_memory", real_page_id)
        )

        # 释放实页
        for virt_page_id, row in pro.page_table.iterrows():
            if row['valid']:
                self.remain_real_page_num += 1
                real_page_id = row['real_page_id']
                self.state[real_page_id] = False
                pro.valid_virt_page_queue.remove(virt_page_id)
                msg_queue.put(
                    ("free_memory", real_page_id)
                )

    # def get_real_page(self, pid: str, bytes_delta: int) -> str | int:
    #     pcb: PCB = self.PCBs[pid]
    #     if pcb.bytes < bytes_delta:
    #         return '越界！'
    #
    #     virt_page = bytes_delta // page_size
    #     real_page = pcb.page_table.loc[virt_page, 'real_page_num']
    #     return real_page


main_mem = MainMemory()
