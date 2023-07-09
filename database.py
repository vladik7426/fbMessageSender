"""This module handles the interaction with the database. It includes functions for retrieving new records from the
database."""
from datetime import date, timedelta, datetime

from _decimal import Decimal
from logging import Logger
from typing import List, Tuple, Set

from config import database_settings
from mysql.connector import connect as mysql_connect
from mysql.connector import CMySQLConnection

CONNECTION: CMySQLConnection | None = None

logger = Logger("database")


def create_connection():
    global CONNECTION

    if CONNECTION is not None:
        logger.warning("Connection exists, but creating new...")

    CONNECTION = mysql_connect(**database_settings['credentials'])


def get_task_rows() -> List[tuple]:
    global CONNECTION

    if CONNECTION is None:
        create_connection()

    cursor = CONNECTION.cursor()

    cursor.execute(f"SELECT * FROM {database_settings['table-names']['tasks']}")

    rows = cursor.fetchall()

    return rows


def get_facebook_group_rows() -> List[tuple]:
    global CONNECTION

    if CONNECTION is None:
        create_connection()

    cursor = CONNECTION.cursor()

    cursor.execute(f"SELECT * FROM {database_settings['table-names']['groups']}")

    rows = cursor.fetchall()

    return rows
