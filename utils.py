import re
from os import path
from urllib import request
from urllib.parse import urlparse


class TaskStatus:
    WAITING = 'WAITING'
    DOING = 'DOING'
    DONE = 'DONE'


def format_task_row(task_row: tuple):
    return {'id': task_row[0],
            'ad': task_row[1],
            'status': task_row[2],
            'created_at': task_row[3],
            'updated_at': task_row[4],
            'photo': task_row[5],
            'title': task_row[6],
            'order': task_row[7]}


def format_fb_group_row(group_row: tuple):
    return {'id': group_row[0],
            'title': group_row[1],
            'url': group_row[2],
            'created_at': group_row[3],
            'updated_at': group_row[4],
            'facebook_search_id': group_row[5],
            'is_run': group_row[6]}
