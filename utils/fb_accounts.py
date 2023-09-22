"""This file contains utility functions for simplifying the usage of Selenium, a web automation tool. It provides
helper functions for common Selenium operations."""
from logging import Logger
from typing import List, Union
from time import time

from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

import database
from config import facebook_config

from threading import Lock

logger = Logger('selenium_utils')
lock = Lock()

__next_account_id = 0


def get_next_cookies():
    """
    :return: returns two values of the next account: c_user, xs
    """
    global __next_account_id

    account: Union[None, tuple] = database.get_account_by_id(__next_account_id)

    last_id = database.get_last_id_in_table("accounts")

    while account is None:
        __next_account_id += 1
        account = database.get_account_by_id(__next_account_id)

        if __next_account_id > last_id:
            __next_account_id = 0

    return account[2], account[3]


def next_account_cookies() -> List[dict]:
    """
    :return: returns next account cookies list;
    """
    global __next_account_id

    c_user, xs = get_next_cookies()

    __next_account_id += 1

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


def init_driver() -> webdriver.Edge:
    lock.acquire()

    options = webdriver.ChromeOptions()
    options.proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': facebook_config['proxy'],
        'ftpProxy': facebook_config['proxy'],
        'sslProxy': facebook_config['proxy'],
        'noProxy': '',
    })

    driver = webdriver.Chrome(options=options)

    driver.get("https://facebook.com")

    for cookie in next_account_cookies():
        driver.add_cookie(cookie)

    lock.release()

    return driver


def get_driver() -> webdriver.Edge | None:
    driver = init_driver()

    return driver
