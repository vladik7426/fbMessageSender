"""This module handles the interaction with the database. It includes functions for retrieving new records from the
database."""
from logging import Logger
from typing import Any, Tuple, Generator, List

from pymysql import connect as mysql_connect
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from config import database_settings
from utils.database_types import QueueRow, TaskRow, FBGroupRow

CONNECTION: Connection | None = None

logger = Logger("database")


def get_connection() -> Connection:
    try:
        global CONNECTION

        if CONNECTION is None:
            CONNECTION = mysql_connect(**database_settings['credentials'],
                                       autocommit=True,
                                       charset='utf8mb4')
            CONNECTION.autocommit(True)

        return CONNECTION
    except Exception:
        return get_connection()


def get_queue_rows(limit: int = 1000) -> list[QueueRow]:
    cursor = execute_query(
        f"SELECT * FROM {database_settings['table-names']['queues']} "
        f"WHERE status IS NULL LIMIT {limit}")

    return [QueueRow(row) for row in cursor.fetchall()]


def get_queue_tasks_by_id(queue_id) -> list[TaskRow]:
    # get task id
    cursor = execute_query(
        f"SELECT * FROM {database_settings['table-names']['queue_tasks']} "
        f"WHERE queue_id={queue_id} AND status is NULL")

    rows = cursor.fetchall()

    task_rows = []
    for row in rows:
        _task_id = row[1]

        # get task
        cursor = execute_query(
            f"SELECT * FROM {database_settings['table-names']['tasks']} "
            f"WHERE id={_task_id}")

        task_rows.append(TaskRow(cursor.fetchone()))
    return task_rows

def get_facebook_groups(queue_id: int, task_id: int, limit=1000) -> list[FBGroupRow]:
    cursor = execute_query(
        f"SELECT * FROM {database_settings['table-names']['task_facebook_groups']} "
        f"WHERE queue_id={queue_id} AND task_id={task_id} LIMIT {limit}")

    group_ids = [int(row[3]) for row in cursor.fetchall()]  # getting facebook_id column from every row

    rows = []
    for group_id in group_ids:
        cursor = execute_query(
            f"SELECT * FROM {database_settings['table-names']['facebook_groups']} "
            f"WHERE id={group_id}")
        rows.append(FBGroupRow(cursor.fetchone()))

    return rows


def get_task_rows() -> tuple[tuple[Any, ...], ...]:
    cursor = execute_query(f"SELECT * FROM {database_settings['table-names']['tasks']} WHERE status is NULL")

    return cursor.fetchall()


def get_facebook_group_rows() -> tuple[tuple[Any, ...], ...]:
    cursor = execute_query(f"SELECT * FROM {database_settings['table-names']['groups']}")

    rows = cursor.fetchall()

    return rows


def set_queue_status_by_queue_id(queue_id, status):
    queries = (
        f"UPDATE {database_settings['table-names']['queues']} SET status='{status}' WHERE id={queue_id}",
        f"UPDATE {database_settings['table-names']['queue_tasks']} SET status='{status}' WHERE queue_id={queue_id}",
    )
    for query in queries:
        execute_query(query)


def set_task_status_by_id(task_id, status):
    execute_query(f"UPDATE {database_settings['table-names']['tasks']} SET status='{status}' WHERE id={task_id}")


def execute_query(query) -> Cursor:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query)

    return cursor
