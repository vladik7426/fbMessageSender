from queue import Queue
from threading import Thread

import database
import facebook
from FBDriver import FBDriver
from config import THREAD_COUNT, QUEUE_MAX_LEN
from utils import fb_accounts
from utils.database_types import FBGroupTaskRowPair, TaskStatus


def handle_thread(queue):
    driver = FBDriver()
    while True:
        if queue.qsize() > 0:
            queue_value: FBGroupTaskRowPair = queue.get()
            if isinstance(queue_value, FBGroupTaskRowPair):
                fb_groups, task_row = queue_value.get_pair()
                execute_task(driver, queue_value, task_row, fb_groups)


def execute_task(driver, queue_value, task_row, fb_groups):
    for fb_group in fb_groups:
        try:
            facebook.send_ad_to_group(driver, fb_group, task_row)

            database.set_queue_status_by_queue_id(queue_value.get_queue_id(), TaskStatus.DONE)
            database.set_task_status_by_id(task_row.id, TaskStatus.DONE)
        except Exception:
            database.set_queue_status_by_queue_id(queue_value.get_queue_id(), TaskStatus.ERROR)
            database.set_task_status_by_id(task_row.id, TaskStatus.ERROR)


def main():
    queue = Queue()
    threads = (Thread(target=handle_thread, args=(queue,)) for _ in range(THREAD_COUNT))

    for thread in threads:
        thread.start()

    while True:
        queue_can_contain = QUEUE_MAX_LEN - queue.qsize()
        if queue_can_contain > 0:
            queue_rows = database.get_queue_rows(limit=1)

            if len(queue_rows) > 0:
                queue_row = queue_rows[0]

                task_rows = database.get_queue_tasks_by_id(queue_row.id)

                for task_row in task_rows:
                    database.set_queue_status_by_queue_id(queue_row.id, TaskStatus.DOING)
                    database.set_task_status_by_id(task_row.id, TaskStatus.DOING)

                    if task_row is not None:
                        fb_groups = database.get_facebook_groups(queue_row.id, task_row.id)
                        queue.put(FBGroupTaskRowPair(fb_groups, task_row, queue_row.id))


if __name__ == '__main__':
    main()
