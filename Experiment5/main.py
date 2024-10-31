from pre import *
from schedules import *

""" 进程调度算法程序说明

依赖结构如下：
├── ./in
├── ./out
├── ./std
├── main.py
├── pre.py
├── schedules.py

其中 `./in` 是输入文件夹 `./out` 是输出文件夹 `./std` 是标答文件夹。

`main.py` 是程序的入口部分，负责人机交互选择合适的算法测试数据；
`pre.py` 是程序的框架部分，负责构造进程类、I/O 逻辑和测试逻辑；
`schedules.py` 是程序的算法部分，负责 7 个调度算法的逻辑。

"""

def main(test_size: int=2) -> None:
    while True:
        display_menu()
        choose = input()
        switch = {
            '1': FCFS,
            '2': SJF,
            '3': SRTF,
            '4': HRRF,
            '5': Pr,
            '6': RR,
            '7': MLFQ,
            '0': None
        }
        if choose not in switch:
            print("输入错误，请重新输入！")
            continue
        elif choose == '0':
            break
        for id in range(1, test_size + 1):
            processes = load_process(f'./in/{id}.in')
            results = switch[choose](processes)
            write_process(f'./out/{id}.out', results)
            print(f"test{id}:")
            checker(f'./out/{id}.out', f'./std/{id}-{switch[choose].__name__}.std')

if __name__ == '__main__':
    main(test_size=2)
