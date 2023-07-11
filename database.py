"""This module handles the interaction with the database. It includes functions for retrieving new records from the
database."""
from logging import Logger
from typing import List, Final, Tuple, Any

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


def get_task_rows() -> tuple[tuple[Any, ...], ...]:
    conn = execute_query(f"SELECT * FROM {database_settings['table-names']['tasks']}")

    rows = conn.cursor().fetchall()

    return rows


def get_facebook_group_rows() -> tuple[tuple[Any, ...], ...]:
    conn = execute_query(f"SELECT * FROM {database_settings['table-names']['groups']}")

    rows = conn.cursor().fetchall()

    return rows


def set_task_status(task_id, status):
    execute_query(
        f"UPDATE {database_settings['table-names']['tasks']} SET status = '{status}' WHERE id={task_id}")


def execute_query(query) -> Connection:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(query)

    return connection
