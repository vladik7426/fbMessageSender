"""This module handles the interaction with the database. It includes functions for retrieving new records from the
database."""
from logging import Logger
from typing import List

from pymysql import connect as mysql_connect
from pymysql.connections import Connection

from config import database_settings

logger = Logger("database")


def create_connection() -> Connection:
    try:
        return mysql_connect(**database_settings['credentials'],
                             autocommit=True,
                             charset='utf8mb4')
    except Exception:
        return create_connection()


def get_task_rows() -> List[tuple]:
    conn, cursor = execute_query(f"SELECT * FROM {database_settings['table-names']['tasks']}")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def get_facebook_group_rows() -> List[tuple]:
    conn, cursor = execute_query(f"SELECT * FROM {database_settings['table-names']['groups']}")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def set_task_status(task_id, status):
    conn, cursor = execute_query(f"UPDATE {database_settings['table-names']['tasks']} SET status = '{status}' WHERE id={task_id}")
    cursor.close()
    conn.close()


def execute_query(query) -> tuple:
    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(query)

    return connection, cursor
