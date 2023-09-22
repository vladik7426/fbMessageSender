"""This file is used for storing project configurations. You can define variables or constants related to the
project's settings, such as database credentials, API keys, or other configurable options."""
from dataclasses import dataclass

THREAD_COUNT = 5
QUEUE_MAX_LEN = 10

facebook_settings = []

facebook_settings = {
    "cookie": {
        'c_user': '100093921954323',
        'xs': '17%3A25Ii_fJNjaWa0w%3A2%3A1689174300%3A-1%3A-1%3A%3AAcXFyihurwp70p1wYfppIv7ozOsGGMWTxnoeLapl2Q',
    },
    "proxy": "",
}

database_settings = {
    'credentials': {
        'user': 'root',
        'password': '13245',
        'host': 'localhost',
        'database': 'pup',
    }
}


@dataclass
class _FacebookSettings:
    @dataclass
    class _FacebookCookies:
        c_user: str
        xs: str

    cookies: _FacebookCookies
    proxy: str


@dataclass
class _DatabaseSettings:
    @dataclass
    class _DatabaseCredentials:
        user: str
        password: str
        host: str
        database: str
