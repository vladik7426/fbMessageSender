"""This module handles the interaction with the database. It includes functions for retrieving new records from the
database."""
import logging
from logging import Logger
from typing import Any, Union

from pymysql import connect as mysql_connect, ProgrammingError
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from config import database_settings
from utils.database_types import QueueRow, TaskRow, FBGroupRow

logger = Logger("database")


def get_connection() -> Connection:
    return mysql_connect(**database_settings['credentials'],
                         autocommit=True,
                         charset='utf8mb4')


def execute_query(query) -> Union[Cursor, None]:
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        return cursor
    except ProgrammingError as ex:
        logging.error(f"Error occurred while executing query: {query}! " + str(ex))

    return None


def get_queue_rows(limit: int = 1000) -> list[QueueRow]:
    cursor = execute_query(
        f"SELECT * FROM queues "
        f"WHERE status IS NULL LIMIT {limit}")

    return [QueueRow(row) for row in cursor.fetchall()]


def get_queue_tasks_by_id(queue_id) -> list[TaskRow]:
    # get task id
    cursor = execute_query(
        f"SELECT * FROM queue_tasks "
        f"WHERE queue_id={queue_id} AND status is NULL")

    rows = cursor.fetchall()

    task_rows = []
    for row in rows:
        _task_id = row[1]

        # get task
        cursor = execute_query(
            f"SELECT * FROM tasks "
            f"WHERE id={_task_id}")

        task_rows.append(TaskRow(cursor.fetchone()))
    return task_rows


def get_facebook_groups(queue_id: int, task_id: int, limit=1000) -> list[FBGroupRow]:
    cursor = execute_query(
        f"SELECT * FROM task_facebook_groups "
        f"WHERE queue_id={queue_id} AND task_id={task_id} LIMIT {limit}")

    group_ids = [int(row[3]) for row in cursor.fetchall()]  # getting facebook_id column from every row

    rows = []
    for group_id in group_ids:
        cursor = execute_query(
            f"SELECT * FROM facebook_groups "
            f"WHERE id={group_id}")
        rows.append(FBGroupRow(cursor.fetchone()))

    return rows


def get_task_rows() -> tuple[tuple[Any, ...], ...]:
    cursor = execute_query(f"SELECT * FROM tasks WHERE status is NULL")

    return cursor.fetchall()


def get_facebook_group_rows() -> tuple[tuple[Any, ...], ...]:
    cursor = execute_query(f"SELECT * FROM groups")

    rows = cursor.fetchall()

    return rows


def set_queue_status_by_queue_id(queue_id, status):
    queries = (
        f"UPDATE queues SET status='{status}' WHERE id={queue_id}",
        f"UPDATE queue_tasks SET status='{status}' WHERE queue_id={queue_id}",
    )
    for query in queries:
        execute_query(query)


def set_task_status_by_id(task_id, status):
    execute_query(f"UPDATE tasks SET status='{status}' WHERE id={task_id}")


def get_account_by_id(account_id: int) -> Union[tuple, None]:
    """
    :return: (id, usage, c_user, xs, ip_username, ip_password, ip_port, comment, created_at, updated_at, is_proxy_ok,
    is_blocked) or None if account with this id is not exists
    """

    cursor = execute_query(f"SELECT * FROM accounts WHERE id={account_id}")

    if cursor is not None and cursor.rowcount > 0:
        return cursor.fetchone()

    return None


def get_last_id_in_table(table_name) -> Union[int, None]:
    cursor = execute_query(f"SELECT `id` FROM {table_name}")

    if cursor is not None:
        return cursor.fetchone()[0]

    return None
