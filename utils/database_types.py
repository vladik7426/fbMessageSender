from typing import Tuple, List


class TaskStatus:
    DOING = 'DOING'
    DONE = 'DONE'
    ERROR = 'ERROR'


class QueueRow:
    def __init__(self, queue_row: tuple | list):
        self.id = queue_row[0]
        self.status = queue_row[1]


class TaskRow:
    def __init__(self, task_row: tuple | list):
        self.id = task_row[0]
        self.ad = task_row[1]
        self.status = task_row[2]
        self.created_at = task_row[3]
        self.updated_at = task_row[4]
        self.photo = task_row[5]


class FBGroupRow:
    def __init__(self, group_row: tuple | list) -> object:
        self.id = group_row[0]
        self.title = group_row[1]
        self.url = group_row[2]
        self.created_at = group_row[3]
        self.updated_at = group_row[4]
        self.facebook_search_id = group_row[5]
        self.is_run = group_row[6]


class FBGroupTaskRowPair:
    def __init__(self, fb_groups: list[FBGroupRow], task_row: TaskRow, queue_id=None):
        if isinstance(fb_groups, list | tuple) and isinstance(task_row, TaskRow):
            self._fb_groups = fb_groups
            self._task_row = task_row
            self._queue_id = queue_id
        else:
            raise RuntimeError("FBGroupTaskPair: cannot init pair with given types: "
                               f"{type(fb_groups)} and {type(task_row)}")

    def get_pair(self) -> tuple[list[FBGroupRow], TaskRow]:
        return self._fb_groups, self._task_row

    def get_queue_id(self) -> int:
        return self._queue_id
