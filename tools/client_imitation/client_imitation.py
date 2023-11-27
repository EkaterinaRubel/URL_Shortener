"""Модуль для иммитации запросов от клиента."""
import asyncio
import logging
from urllib.parse import urljoin

from httpx import AsyncClient

from src.app.config.config_api import MAIN_URL
from src.app.logic.generators_short_url import generate_short_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_short_url():
    """
    Отправляет POST-запрос к эндпоинту '/shorten/'.

    Получает короткий URL из длинного URL.
    """
    async with AsyncClient() as ac:
        endpoint_shorten = '/shorten/'
        response = await ac.post(
            urljoin(MAIN_URL, endpoint_shorten),
            json={'long_url': 'https://www.example.com'},
        )
        logger.info(f'Status code: {response.status_code}')
        logger.info(f'response.json: {response.json()}')


async def redirect():
    """Имитирует перенаправление, следуя короткому URL."""
    async with AsyncClient() as ac:
        shorted_url = generate_short_url('https://www.example.com/')
        response = await ac.get(
            urljoin(MAIN_URL, shorted_url),
        )
        logger.info(f'Status code: {response.status_code}')
        logger.info(f'Location header: {response.headers.get("Location")}')


async def get_metrics():
    """Получает метрики сервиса с эндпоинта '/metrics'."""
    async with AsyncClient() as ac:
        endpoint_metrics = '/metrics'
        response = await ac.get(
            urljoin(MAIN_URL, endpoint_metrics),
        )
        logger.info(f'Status code: {response.status_code}')
        logger.info(response.text)

if __name__ == '__main__':
    asyncio.run(get_short_url())
    asyncio.run(redirect())
    asyncio.run(get_metrics())
