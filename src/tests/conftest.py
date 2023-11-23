"""Тестовые фикстуры."""
import asyncio

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager

from src.app.main import app


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
