"""Config for DB."""

import os
from dataclasses import dataclass

from pydantic import PostgresDsn

db_name = os.environ.get('POSTGRES_DB_NAME')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_login = os.environ.get('POSTGRES_USER')
db_host = os.environ.get('POSTGRES_HOST')


@dataclass
class PostgresConfig(object):
    """
    Класс для хранения настроек подключения к PostgreSQL базе данных.

    Attributes:
        password (str): Пароль для доступа к базе данных.
        login (str): Имя пользователя базы данных.
        host (str): Адрес хоста базы данных.
        port (int): Порт подключения к базе данных.
        name (str): Имя базы данных.

    Properties:
        url (str): URL для подключения к базе данных.
        uri (str): URI для подключения к базе данных с использованием asyncpg.
    """

    password: str = db_password
    login: str = db_login
    host: str = db_host
    port: int = 5432
    name: str = db_name

    @property
    def url(self) -> str:
        """
        Возвращает URL для подключения к базе данных.

        Returns:
            str: URL.
        """
        temp_url = str(PostgresDsn.build(
            scheme='temp',
            username=self.login,
            password=self.password,
            host=self.host,
            port=int(self.port),
        ))
        return temp_url.replace('temp://', '')

    @property
    def uri(self) -> str:
        """
        Возвращает URI для подключения к базе данных с использованием asyncpg.

        Returns:
            str: URI для подключения с использованием asyncpg.
        """
        return str(PostgresDsn.build(
            scheme='postgresql',
            username=self.login,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        ))


@dataclass
class AppConfig(object):
    """
    Представляет конфигурацию подключения к БД PostgreSQL.

    Attributes:
        postgres (PostgresConfig): Настройки подключения к БД PostgreSQL.
    """

    postgres: PostgresConfig


app_config = AppConfig(
    postgres=PostgresConfig(),
)
