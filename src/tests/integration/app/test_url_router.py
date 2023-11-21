"""Модуль тестирования endpoints обработки url."""
import pytest
from httpx import AsyncClient

from src.app.config.config_api import MAIN_URL
from src.app.logic.generators_short_url import generate_short_url
from src.app.main import app


@pytest.mark.asyncio
async def test_create_short_url():
    """Тестирует эндпоинт для создания короткого URL."""
    long_url = 'https://www.example.com/'
    async with AsyncClient(app=app, base_url='http://testing') as ac:
        response = await ac.post(
            '/shorten/',
            json={'long_url': long_url},
        )
        short_url = generate_short_url(long_url)
        assert response.text.strip('"') == f'{MAIN_URL}/{short_url}'


@pytest.mark.asyncio
async def test_read_short_url():
    """Тестирует эндпоинт для получения исходного URL по короткому URL."""
    long_url = 'http://www.testing.com/'
    short_url = generate_short_url(long_url)
    async with AsyncClient(
        app=app,
        base_url='http://test',
        follow_redirects=False,
    ) as ac:
        response = await ac.get(short_url)
        assert response.status_code == 301
        assert response.headers['Location'] == long_url
