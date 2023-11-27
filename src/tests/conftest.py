"""Тестовые фикстуры."""
import asyncio

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager

from src.app.main import app
from src.data_base.connections.connections import db_manager
from src.tests.tests_config import SHORTED_URL


@pytest.fixture(scope='session')
def event_loop():
    """
    Создает экземпляр event loop с scope='session'.

    Так как встроенная фикстура имеет scope='function'

    Yields:
        asyncio.AbstractEventLoop: Экземпляр event loop.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def initialize_lifespan():
    """
    Инициализирует lifespan перед тестами.

    Без - lifespan не инициализируется, так как
    при использовании AsyncClient сервис не запускается.

    Yields:
        FastAPI: Инициализированный экземпляр FastAPI приложения.
    """
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture(scope='session')
async def connection(initialize_lifespan):
    """
    Возвращает соединение с базой данных.

    Args:
        initialize_lifespan: Инициализированный экземпляр FastAPI приложения.

    Yields:
        connection
    """
    async with db_manager.get_db_connection() as conn:
        yield conn


@pytest_asyncio.fixture(scope='session')
async def new_db_schema(connection):
    """
    Cоздает схемы данных в тестовой базе и удаляет их после завершения тестов.

    А так же возвращает connection на время тестов

    Args:
        connection: соединение с базой данных

    Yields:
        None
    """
    conn = connection
    await conn.execute("""
        DROP SEQUENCE IF EXISTS url_id_seq;
        DROP TABLE IF EXISTS url_mapping;
        CREATE SEQUENCE url_id_seq;

        CREATE TABLE url_mapping (
            url_id BIGINT PRIMARY KEY DEFAULT nextval('url_id_seq'),
            short_url VARCHAR(255) UNIQUE NOT NULL,
            long_url VARCHAR(255) NOT NULL,
            creation_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            click_count BIGINT DEFAULT 0 NOT NULL
        );
        CREATE INDEX idx_short_url ON url_mapping (short_url);
    """)
    yield
    await conn.execute("""
        DROP TABLE url_mapping;
        DROP SEQUENCE url_id_seq;
    """)


@pytest_asyncio.fixture(scope='session')
async def put_url_map(connection, new_db_schema):
    """
    Вставляет данные в таблицу url_mapping перед тестами и удаляет их после.

    Args:
        connection: соединение с базой данных
        new_db_schema: таблица в БД

    Yields:
        None
    """
    conn = connection
    await conn.execute(
        "INSERT INTO url_mapping (short_url, long_url) \
            VALUES ($1, 'http://www.testing.com/');",  # noqa: WPS318
        SHORTED_URL,
    )
    yield
    await conn.execute(
        'DELETE FROM url_mapping WHERE short_url = $1',
        SHORTED_URL,
    )
