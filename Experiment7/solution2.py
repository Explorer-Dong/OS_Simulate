import threading
import time, sys

r"""
python solution2.py word1.txt word2.txt && python main.py
"""

write_mutex = threading.Semaphore(1)
print_step = True

def count_words(file_path, cnt: list[int], no: int) -> None:
    start_time = time.time()
    time_step = []

    with open(file_path, 'r') as f:
        last = ' '
        while last:
            char = f.read(1)
            time.sleep(0.01 if print_step else 0)

            if not char.isalnum() and last.isalnum():
                cnt[no] += 1
                del_t = int((time.time() - start_time) * 1000)
                time_step.append(del_t)
                if print_step:
                    print(f"{threading.current_thread().name} update {del_t}")
            
            last = char
    
        # 互斥写入文件
        write_mutex.acquire()
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
    count = [0, 0]
    thread1 = threading.Thread(target=count_words, args=(file1, count, 0), name='t1')
    thread2 = threading.Thread(target=count_words, args=(file2, count, 1), name='t2')

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Total words", sum(count))
