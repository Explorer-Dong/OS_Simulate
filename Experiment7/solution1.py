import threading
import time, sys

r"""
cd Experiment7
python solution1.py word1.txt word2.txt && python main.py
"""

total_words = 0
mutex = threading.Semaphore(1)
write_mutex = threading.Semaphore(1)
print_step = True

def count_words_in_file(file_path: str) -> None:
    now_words = 0
    start_time = time.time()
    time_step = []

    def count() -> None:
        nonlocal now_words
        mutex.acquire()
        now_words += 1
        del_t = int((time.time() - start_time) * 1000)
        time_step.append(del_t)
        if print_step:
            print(f"{threading.current_thread().name} update {del_t}")
        mutex.release()

    with open(file_path, 'r') as file:
        last = ' '
        while last:
            char = file.read(1)

            time.sleep(0.01 if print_step else 0)
            if not char:
                if last.isalnum():
                    count()
                break

            if not char.isalnum() and last.isalnum():
                count()
            
            last = char
        
        # 互斥写入文件
        write_mutex.acquire()
        global total_words
        total_words += now_words
        file_name = file_path.split('/')[-1]
        with open('./ans.out', 'a') as out_file:
            out_file.write("File$$" + file_name + "$$: ")
            for t in time_step:
                # print(t)
                out_file.write(str(t) + ' ')
            out_file.write('\n')
            print(f"write {file_name} down")
        write_mutex.release()

if __name__ == '__main__':
    open('./ans.out', 'w')
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    thread1 = threading.Thread(target=count_words_in_file, args=(file1, ), name='t1')
    thread2 = threading.Thread(target=count_words_in_file, args=(file2, ), name='t2')

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Total words:", total_words)
