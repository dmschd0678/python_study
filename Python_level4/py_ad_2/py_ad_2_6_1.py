"""
Section 2
Parallelism with Multiprocessing - multiprocessing(5) - Queue, Pipe
Keyword - Queue, Pipe, Communications between processes
"""

# 프로세스 통신 구현 Queue

from multiprocessing import Process, Queue,current_process
import time
import os

# 실행 함수
def worker(id, baseNum, q):
    process_id = os.getpid()
    process_name = current_process().name

    # 누적
    sub_total = 0

    # 계산
    for i in range(baseNum):
        sub_total += 1

    # Produce
    q.put(sub_total)

    # 정보 출력
    print(f"process ID : {process_id}, Process Name : {process_name} ID : {id}")

    print(f"Result : {sub_total}")

def main():
    # 부모 프로세스 id
    parent_process = os.getpid()
    # 출력
    print(f"Parent process ID : {parent_process}")

    # 프로세스 리스트 선언
    processes = []

    # 시작 시간
    start_time = time.time()

    # Queue 선언
    q = Queue()

    for i in range(5): # 1 ~ 100 컴퓨터 사양의 맞게 조절
        # 생성
        t = Process(name = str(i), target=worker, args = (i,100000000,q))

        # 배열에 담기
        processes.append(t)

        # 시작
        t.start()

    for process in processes:
        process.join()

    # 순수 계산 시간
    print("--- %s seconds ---" % (time.time() - start_time))

    # 종료 플래그
    q.put('exit')

    total = 0

    # 대기
    while True:
        tmp = q.get()
        if tmp == 'exit':
            break
        else:
            total += tmp
    print()

    print("Main processing Total Count = {}".format(total))
    print("Main processing Done")
if __name__ == "__main__":
    main()