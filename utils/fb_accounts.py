"""This file contains utility functions for simplifying the usage of Selenium, a web automation tool. It provides
helper functions for common Selenium operations."""
from threading import Lock
from time import time
from typing import List, Union

import database

_lock = Lock()

_next_account_id = 0


def _get_next_cookies():
    """
    :return: returns two values of the next account: c_user, xs
    """
    global _next_account_id

    account: Union[None, tuple] = database.get_account_by_id(_next_account_id)

    last_id = database.get_last_id_in_table("accounts")

    while account is None:
        _next_account_id += 1
        account = database.get_account_by_id(_next_account_id)

        if _next_account_id > last_id:
            _next_account_id = 0

    return account[2], account[3]


def next_account_cookies() -> List[dict]:
    """
    :return: returns next account cookies list;
    """
    _lock.acquire()

    global _next_account_id

    c_user, xs = _get_next_cookies()

    _next_account_id += 1

    _lock.release()

    return [
        {
            'name': 'c_user',
            'value': c_user,
            'domain': '.facebook.com',
            'path': '/',
            'expires': int(time()) + 100000000,
            'httpOnly': True,
            'secure': True,
            'session': False,
            'sameSite': 'None',
            'sameParty': False,
            'sourceScheme': 'Secure',
            'sourcePort': 443
        },
        {
            'name': 'xs',
            'value': xs,
            'domain': '.facebook.com',
            'path': '/',
            'expires': int(time()) + 100000000,
            'httpOnly': True,
            'secure': True,
            'session': False,
            'sameSite': 'None',
            'sameParty': False,
            'sourceScheme': 'Secure',
            'sourcePort': 443
        }
    ]
