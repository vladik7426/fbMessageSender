"""This file is used for storing project configurations. You can define variables or constants related to the
project's settings, such as database credentials, API keys, or other configurable options."""
from dataclasses import dataclass


# region "local dataclasses"
@dataclass
class _FacebookCookies:
    c_user: str
    xs: str


@dataclass
class _FacebookConfig:
    cookies: _FacebookCookies
    proxy: str


@dataclass
class _DatabaseCredentials:
    user: str
    password: str
    host: str
    database: str

    def as_dict(self) -> dict:
        return {attr: self.__getattribute__(attr)
                for attr in self.__annotations__}


@dataclass
class _DatabaseConfig:
    credentials: _DatabaseCredentials


# endregion


# region "configs"

THREAD_COUNT = 1
QUEUE_MAX_LEN = 10

facebook_config = _FacebookConfig(
    cookies=_FacebookCookies(
        c_user='100093921954323',
        xs='17%3A25Ii_fJNjaWa0w%3A2%3A1689174300%3A-1%3A-1%3A%3AAcXFyihurwp70p1wYfppIv7ozOsGGMWTxnoeLapl2Q'),
    proxy='',
)

database_config = _DatabaseConfig(
    credentials=_DatabaseCredentials(
        user='root',
        password='13245',
        host='127.0.0.1',
        database='pup')
)

# endregion
