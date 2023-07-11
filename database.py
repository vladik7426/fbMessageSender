"""This module handles the interaction with the database. It includes functions for retrieving new records from the
database."""
from logging import Logger
from typing import Any, Tuple, Generator

from pymysql import connect as mysql_connect
from pymysql.connections import Connection

from config import database_settings

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


def get_queue_rows(limit: int = 100) -> tuple[tuple[Any, ...], ...]:
    conn = execute_query(
        f"SELECT * FROM {database_settings['table-names']['queues']} WHERE status IS NULL LIMIT {limit}")

    return conn.cursor().fetchall()


def get_facebook_group_ids(queue_id: int, task_id: int) -> Generator[int]:
    conn = execute_query(
        "SELECT * FROM {database_settings['table-names']['task_facebook_groups']}"
        f"WHERE queue_id={queue_id} AND task_id={task_id}")

    return (int(row[3]) for row in conn.cursor().fetchall())  # getting facebook_id column from every row


def get_task_rows() -> tuple[tuple[Any, ...], ...]:
    conn = execute_query(f"SELECT * FROM {database_settings['table-names']['tasks']}")

    return conn.cursor().fetchall()


def get_facebook_group_rows() -> tuple[tuple[Any, ...], ...]:
    conn = execute_query(f"SELECT * FROM {database_settings['table-names']['groups']}")

    rows = conn.cursor().fetchall()

    return rows


def set_task_status(task_id, status):
    queries = (
        f"UPDATE {database_settings['table-names']['queues']} SET status='{status}' WHERE task_id={task_id}",
        f"UPDATE {database_settings['table-names']['queue_tasks']} SET status='{status}' WHERE task_id={task_id}",
        f"UPDATE {database_settings['table-names']['tasks']} SET status='{status}' WHERE id={task_id}",
    )
    for query in queries:
        execute_query(query)


def execute_query(query) -> Connection:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query)

    return connection
