from main_memory import MainMemory

"""r
测试样例输入：
>>> 1
    a 5000
    1
    b 38400
    1
    c 49700
    1
    d 11000
    2
    b
    1
    d 25000
    1
    e 16000
    2
    a
    1
    f 10000
    4
    e 15437
    4
    c 50000
    3

标准输出：
>>> 1
    a 5000
    1
    b 38400
    1
    c 49700
    1
    d 11000
    内存不够分配
    2
    b
    1
    d 25000
    1
    e 16000
    2
    a
    1
    f 10000
    内存不够分配
    4
    e 15437
    物理地址为95437
    4
    c 50000
    越界！
    3
    作业名  占用页面数      占用页框号
    c       50      [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93]
    d       25      [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
    e       16      [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 94, 95]
"""

real_page_num = 100  # 实页（页框）数
page_size = 1000     # 页面大小（字节）
main_mem = MainMemory(real_page_num=real_page_num, page_size=page_size)

if __name__ == '__main__':
    while True:
        op = input().strip()
        if op == '0':
            break
        elif op == '1':
            info = input().strip().split()
            pid, bytes = info[0], int(info[1])
            state = main_mem.allocate(pid, bytes)
            if state is not None:
                print(state)
        elif op == '2':
            pid = input().strip()
            main_mem.free(pid)
        elif op == '3':
            main_mem.show()
        elif op == '4':
            info = input().strip().split()
            pid, bytes_delta = info[0], int(info[1])
            result = main_mem.get_real_page(pid, bytes_delta)
            if type(result) == str:
                print(result)
            else:
                delta = bytes_delta % page_size
                real_address = str(result) + str(delta)
                print(f'物理地址为{real_address}')
        else:
            print('无效输入，请重新输入！')
