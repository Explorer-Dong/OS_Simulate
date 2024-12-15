import pandas as pd

class PCB:
    def __init__(self, pid: str, bytes: int):
        self.pid = pid                    # 进程编号
        self.bytes = bytes                # 进程实际所需字节数
        self.page_table = pd.DataFrame({  # 进程页表
            'valid': [False] * 200,
            'real_page_num': [None] * 200
        })
