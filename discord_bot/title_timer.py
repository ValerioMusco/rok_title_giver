from collections import deque
import time

def timer_handler(timer_id, fifo_queue: deque, timeout):
    while True:
        time.sleep(timeout)
        print(fifo_queue)
        if len(fifo_queue) != 0:
            item = fifo_queue.popleft()
        else:
            continue
