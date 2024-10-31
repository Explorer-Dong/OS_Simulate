from pre import Process
import heapq
from collections import deque

def FCFS(processes: list[Process]) -> list[Process]:
    """ 先来先服务调度 (非抢占式) """

    # 新建态进程队列
    newPCB = deque(sorted(processes, key=lambda p: p.arrival_time))
    # 就绪态进程队列
    readyPCB = deque()

    res = []
    time = 0
    while len(res) < len(processes):
        # 取出就绪队列的队头进程
        if len(readyPCB) == 0:
            pro = newPCB.popleft()
            readyPCB.append(pro)
        now_pro = readyPCB.popleft()
    
        # 维护时钟和进程信息
        time = max(time, now_pro.arrival_time)
        now_pro.start_time = time
        time += now_pro.service_time
        now_pro.finish_time = time
        res.append(now_pro)
    
        # 更新就绪队列信息
        while len(newPCB) and newPCB[0].arrival_time <= time:
            pro = newPCB.popleft()
            readyPCB.append(pro)
    
    return res

def SJF(processes: list[Process]) -> list[Process]:
    """ 短时间优先调度 (非抢占式) """
    
    # 新建态进程队列
    newPCB = deque(sorted(processes, key=lambda p: (p.arrival_time, p.service_time)))
    # 就绪态进程队列
    readyPCB = []

    res = []
    time = 0
    while len(res) < len(processes):
        # 取出就绪队列的队头进程
        if len(readyPCB) == 0:
            pro = newPCB.popleft()
            heapq.heappush(readyPCB, (pro.service_time, pro.arrival_time, pro))
        now_pro: Process = heapq.heappop(readyPCB)[-1]

        # 维护时钟和进程信息
        time = max(time, now_pro.arrival_time)
        now_pro.start_time = time
        time += now_pro.service_time
        now_pro.finish_time = time
        res.append(now_pro)
    
        # 更新就绪队列信息
        while len(newPCB) and newPCB[0].arrival_time <= time:
            pro = newPCB.popleft()
            heapq.heappush(readyPCB, (pro.service_time, pro.arrival_time, pro))
    
    return res

def SRTF(processes: list[Process]) -> list[Process]:
    """ 最短剩余时间优先调度 (抢占式) """

    # 新建态进程队列
    newPCB = deque(sorted(processes, key=lambda p: (p.arrival_time, p.service_time)))
    # 就绪态进程队列
    readyPCB = []

    res = []
    time = 0
    while len(res) < len(processes):
        # 取出就绪队列的队头进程
        if len(readyPCB) == 0:
            pro = newPCB.popleft()
            heapq.heappush(readyPCB, (pro.service_time - pro.running_time, pro.arrival_time, pro))
        now_pro: Process = heapq.heappop(readyPCB)[-1]

        # 维护时钟和进程信息 & 更新就绪队列信息
        time = max(time, now_pro.arrival_time)
        seized = False
        while len(newPCB):
            pro = newPCB[0]
            if pro.arrival_time >= time + (now_pro.service_time - now_pro.running_time):
                break
            elif pro.service_time >= now_pro.service_time - now_pro.running_time - (pro.arrival_time - time):
                newPCB.popleft()
                heapq.heappush(readyPCB, (pro.service_time - pro.running_time, pro.arrival_time, pro))
            else:
                seized = True
                now_pro.running_time += pro.arrival_time - time
                if now_pro.running_time and now_pro.start_time == None:
                    now_pro.start_time = time
                time += pro.arrival_time - time
                heapq.heappush(readyPCB, (now_pro.service_time - now_pro.running_time, now_pro.arrival_time, now_pro))
                newPCB.popleft()
                heapq.heappush(readyPCB, (pro.service_time - pro.running_time, pro.arrival_time, pro))
                break
        if not seized:
            if now_pro.start_time == None:
                now_pro.start_time = time
            now_pro.finish_time = time + (now_pro.service_time - now_pro.running_time)
            time = now_pro.finish_time
            res.append(now_pro)
    
    return res

def HRRF(processes: list[Process]) -> list[Process]:
    """ 最高响应比优先调度 (非抢占式) """

    # 新建态进程队列
    newPCB = deque(sorted(processes, key=lambda p: p.arrival_time))
    # 就绪态进程队列
    readyPCB = []

    res = []
    time = 0
    while len(res) < len(processes):
        # 取出就绪队列的队头进程
        if len(readyPCB) == 0:
            pro = newPCB.popleft()
            heapq.heappush(readyPCB, (-1, pro))  # -1 是用来占位的
        now_pro: Process = heapq.heappop(readyPCB)[-1]

        # 维护时钟和进程信息
        time = max(time, now_pro.arrival_time)
        now_pro.start_time = time
        time += now_pro.service_time
        now_pro.finish_time = time
        res.append(now_pro)
    
        # 更新就绪队列信息
        temp = []
        while len(readyPCB):
            _, pro = readyPCB.pop()
            temp.append((-(time - pro.arrival_time) / pro.service_time, pro))
        for new_neg_respinse, pro in temp:
            heapq.heappush(readyPCB, (new_neg_respinse, pro))
        while len(newPCB) and newPCB[0].arrival_time <= time:
            pro = newPCB.popleft()
            heapq.heappush(readyPCB, (-(time - pro.arrival_time) / pro.service_time, pro))
    
    return res

def Pr(processes: list[Process]) -> list[Process]:
    """ 优先级调度 (非抢占式) """

    # 新建态进程队列
    newPCB = deque(sorted(processes, key=lambda p: p.arrival_time))
    # 就绪态进程队列
    readyPCB = []

    res = []
    time = 0
    while len(res) < len(processes):
        # 取出就绪队列的队头进程
        if len(readyPCB) == 0:
            pro = newPCB.popleft()
            heapq.heappush(readyPCB, (-1, pro))  # -1 是用来占位的
        now_pro: Process = heapq.heappop(readyPCB)[-1]

        # 维护时钟和进程信息
        time = max(time, now_pro.arrival_time)
        now_pro.start_time = time
        time += now_pro.service_time
        now_pro.finish_time = time
        res.append(now_pro)
    
        # 更新就绪队列信息
        while len(newPCB) and newPCB[0].arrival_time <= time:
            pro = newPCB.popleft()
            heapq.heappush(readyPCB, (pro.priority, pro))
    
    return res

def RR(processes: list[Process], step: int=4) -> list[Process]:
    """ 轮转调度 (抢占式) """

    # 新建态进程队列
    newPCB = deque(sorted(processes, key=lambda p: p.arrival_time))
    # 就绪态进程队列
    readyPCB = deque()

    res = []
    time = 0
    while len(res) < len(processes):
        # 取出就绪队列的队头进程
        if len(readyPCB) == 0:
            pro = newPCB.popleft()
            readyPCB.append(pro)
        now_pro: Process = readyPCB.popleft()

        # 维护时钟和进程信息 & 更新就绪队列信息
        time = max(time, now_pro.arrival_time)
        now_pro.start_time = time if now_pro.start_time == None else now_pro.start_time
        if now_pro.running_time + step >= now_pro.service_time:
            now_pro.finish_time = time + (now_pro.service_time - now_pro.running_time)
            time += now_pro.service_time - now_pro.running_time
            res.append(now_pro)
        else:
            now_pro.running_time += step
            time += step
            while len(newPCB) and newPCB[0].arrival_time <= time:
                readyPCB.append(newPCB.popleft())
            readyPCB.append(now_pro)

    return res

def MLFQ(processes: list[Process], level: int=3) -> list[Process]:
    """ 多级反馈队列调度 (抢占式)
    共 level 个等级的就绪队列，每一个就绪队列的时间片长度为 2^i
    """

    # 新建态进程队列
    newPCB = deque(sorted(processes, key=lambda p: p.arrival_time))
    # 就绪态进程队列
    readyPCB = [deque() for _ in range(level)]

    res = []
    time = 0
    while len(res) < len(processes):
        # 取出就绪队列的队头进程
        now_pro, now_level = None, None
        for i in range(level):
            if len(readyPCB[i]):
                now_pro, now_level = readyPCB[i].popleft(), i
                break
        if now_pro == None:
            now_pro, now_level = newPCB.popleft(), 0

        # 维护时钟和进程信息 & 更新就绪队列信息
        time = max(time, now_pro.arrival_time)
        now_pro.start_time = time if now_pro.start_time == None else now_pro.start_time
        if now_pro.running_time + (1 << now_level) >= now_pro.service_time:
            # 可以执行完毕
            now_pro.finish_time = time + (now_pro.service_time - now_pro.running_time)
            time += now_pro.service_time - now_pro.running_time
            res.append(now_pro)
        else:
            # 无法执行完毕
            now_pro.running_time += (1 << now_level)
            time += 1 << now_level
            while len(newPCB) and newPCB[0].arrival_time <= time:
                readyPCB[0].append(newPCB.popleft())
            now_level = min(now_level + 1, level - 1)
            readyPCB[now_level].append(now_pro)

    return res
