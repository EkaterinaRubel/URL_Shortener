"""Модуль тестирования работы и готовности сервиса."""
import pytest
from httpx import AsyncClient

from src.app.main import app


@pytest.mark.asyncio
async def test_health_check_up():
    """
    Тестирует эндпоинт /healthz/up.

    на соответствие ожидаемому статусу ответа.
    """
    async with AsyncClient(app=app, base_url='http://testing') as ac:
        endpoint_ready = '/healthz/up'
        response = await ac.get(endpoint_ready)
        assert response.status_code == 200
