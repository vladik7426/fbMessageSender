from threading import Thread

import database
import facebook
from utils import format_task_row, TaskStatus


def send_ad(task: dict):
    facebook.send_messages_with_image(task)

    database.set_task_status(task['id'], TaskStatus.DONE)


def main():
    while task_rows := database.get_task_rows():
        for task_row in task_rows:
            task = format_task_row(task_row)
            if task['status'] == TaskStatus.WAITING:
                database.set_task_status(task['id'], TaskStatus.DOING)
                Thread(target=send_ad, args=(task,)).start()


if __name__ == '__main__':
    main()
