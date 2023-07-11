from queue import Queue
from threading import Thread

import database
from config import THREAD_COUNT, QUEUE_MAX_LEN
from utils import selenium_utils
from utils.database_types import FBGroupTaskRowPair


def handle_thread(queue):
    driver = selenium_utils.get_driver()
    while True:
        if queue.qsize() > 0:
            queue_values: list[FBGroupTaskRowPair] = queue.get()
            for queue_value in queue_values:
                if isinstance(queue_values, FBGroupTaskRowPair):
                    fb_group, task_row = queue_value.get_pair()


def main():
    queue = Queue()
    threads = (Thread(target=handle_thread, args=(queue,)) for _ in range(THREAD_COUNT))

    for thread in threads:
        thread.start()

    while True:
        queue_can_contain = QUEUE_MAX_LEN - queue.qsize()
        if queue_can_contain > 0:
            for row in database.get_queue_rows(limit=queue_can_contain):
                pass


if __name__ == '__main__':
    main()
