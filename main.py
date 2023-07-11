from queue import Queue
from threading import Thread

from config import MAX_THREAD_COUNT
from utils import selenium_utils
from utils.database_types import FBGroupRow, TaskRow


class FBGroupTaskRowPair:
    def __init__(self, fb_group: FBGroupRow, task_row: TaskRow):
        if isinstance(fb_group, FBGroupRow) and isinstance(task_row, TaskRow):
            self._fb_group = fb_group
            self._task_row = task_row
        else:
            raise RuntimeError("FBGroupTaskPair: cannot init pair with given types: "
                               f"{type(fb_group)} and {type(task_row)}")

    def get_pair(self) -> tuple[FBGroupRow, TaskRow]:
        return self._fb_group, self._task_row


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
