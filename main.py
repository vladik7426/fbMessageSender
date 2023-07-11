from queue import Queue
from threading import Thread

from config import MAX_THREAD_COUNT
from utils import selenium_utils
from utils.database_types import FBGroupTaskRowPair


def handle_thread(queue):
    driver = selenium_utils.get_driver()
    while True:
        if queue.qsize() > 0:
            queue_value = queue.get_pair()
            if isinstance(queue_value, FBGroupTaskRowPair):
                fb_group, task_row = queue_value.get_pair()


def main():
    queue = Queue()
    threads = (Thread(target=handle_thread, args=(queue,)) for _ in range(MAX_THREAD_COUNT))

    for thread in threads:
        thread.start()

    while True:
        pass


if __name__ == '__main__':
    main()
