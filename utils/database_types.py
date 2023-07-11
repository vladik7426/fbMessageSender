class TaskStatus:
    WAITING = 'WAITING'
    DOING = 'DOING'
    DONE = 'DONE'


class TaskRow:
    def __init__(self, task_row: tuple | list):
        self.id = task_row[0]
        self.ad = task_row[1]
        self.status = task_row[2]
        self.created_at = task_row[3]
        self.updated_at = task_row[4]
        self.photo = task_row[5]
        self.title = task_row[6]
        self.order = task_row[7]


class FBGroupRow:
    def __init__(self, group_row: tuple | list):
        self.id = group_row[0]
        self.title = group_row[1]
        self.url = group_row[2]
        self.created_at = group_row[3]
        self.updated_at = group_row[4]
        self.facebook_search_id = group_row[5]
        self.is_run = group_row[6]

