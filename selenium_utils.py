"""This file contains utility functions for simplifying the usage of Selenium, a web automation tool. It provides
helper functions for common Selenium operations."""
from logging import Logger
from typing import List
from time import time

from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType

from config import facebook_settings

cookie_dicts: List[dict] =[
    {
        'name': 'c_user',
        'value': facebook_settings['cookie']['c_user'],
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
        'value': facebook_settings['cookie']['xs'],
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

DRIVER = None

logger = Logger('selenium_utils')


def init_driver() -> None:
    global DRIVER

    if DRIVER is not None:
        logger.warning("Driver already exists when initialization new")

    options = webdriver.EdgeOptions()
    options.proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': facebook_settings['proxy'],
        'ftpProxy': facebook_settings['proxy'],
        'sslProxy': facebook_settings['proxy'],
        'noProxy': '',
    })

    DRIVER = webdriver.Edge(options=options)

    DRIVER.get("https://facebook.com")

    for cookie in cookie_dicts:
        DRIVER.add_cookie(cookie)


def get_driver() -> webdriver.Edge | None:
    global DRIVER

    if DRIVER is None:
        init_driver()

    return DRIVER
