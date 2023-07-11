"""This file is used for storing project configurations. You can define variables or constants related to the
project's settings, such as database credentials, API keys, or other configurable options."""

THREAD_COUNT = 5
QUEUE_MAX_LEN = 10

facebook_settings = {
    "cookie": {
        'c_user': '100093921954323',
        'xs': '3%3AnUkxAmLZLB63wg%3A2%3A1688063096%3A-1%3A-1%3A%3AAcVFlwNmSRX6GXkw9UunXYOjujL2M8Mgdq7SyBKuoQ',
    },
    "proxy": "",
}

database_settings = {
    'credentials': {
        'user': 'root',
        'password': '13245',
        'host': 'localhost',
        'database': 'default',
    },
    'table-names': {
        'queues': 'queues',
        'queue_tasks': 'queue_tasks',
        'tasks': 'tasks',
        'task_facebook_groups': 'task_facebook_groups',
    }
}