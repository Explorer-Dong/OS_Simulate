class Process:
    def __init__(self, pid: str,
                 arrival_time: float, service_time: float,
                 priority: int) -> None:
        self.pid = pid
        self.arrival_time = arrival_time  # 进程到达时刻
        self.service_time = service_time  # 预估运行时间
        self.priority = priority  # 进程优先级 (越小越高)
        self.level = 0            # 就绪队列等级
        self.start_time = None    # 运行开始时刻
        # self.start_time = [(s1, t1), (s2, t2), ..., (sx, tx)]
        self.running_time = 0     # 已运行时间
        self.finish_time = None   # 运行结束时刻

def load_process(path: str) -> list[Process]:
    processes = []
    with open(path, 'r') as file:
        for line in file:
            pid, arrival_time, service_time, priority = line.split()
            process = Process(pid, int(arrival_time), int(service_time), int(priority))
            processes.append(process)
    return processes

def write_process(path: str, results: list[Process]) -> None:
    with open(path, 'w') as file:
        for pro in results:
            line = f'{pro.pid} {pro.arrival_time} {pro.start_time} {pro.finish_time}'
            file.write(line + '\n')

def display_menu() -> None:
    print("1 先到先服务 FCFS")
    print("2 短作业优先 SJF")
    print("3 最短剩余时间优先 SRTF")
    print("4 最高响应比优先 HRRF")
    print("5 优先级调度 Pr")
    print("6 轮转调度 RR")
    print("7 多级反馈队列调度 MLFQ")
    print("0 退出")
    print("请输入调度算法编号：")

def checker(outPath: str, stdPath: str) -> None:
    with open(outPath, 'r') as outFile, open(stdPath, 'r') as stdFile:
        outLines = outFile.readlines()
        stdLines = stdFile.readlines()
        answer = {}
        output_answer = {}
        for line in stdLines:
            line = line.split()
            # line: (pid, arrival_time, start_time, finish_time)
            answer.update({line[0]: [line[1], line[2], line[3]]})
        for line in outLines:
            line = line.split()
            output_answer.update({line[0]: [line[1], line[2], line[3]]})
        for pid, info in answer.items():
            if pid not in output_answer or output_answer[pid] != info:
                print(f"process '{pid}' ×")
            else:
                print(f"process '{pid}' √")
