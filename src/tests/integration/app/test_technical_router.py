"""Модуль тестирования работы и готовности сервиса."""
from unittest.mock import AsyncMock, patch
from urllib.parse import urljoin

import pytest
from httpx import AsyncClient

from src.app.config.config_api import MAIN_URL
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


@pytest.mark.asyncio
async def test_health_check_ready_integration(initialize_lifespan):
    """
    Тестирует эндпоинт /healthz/ready.

    Для успешного прохождения БД должна быть доступна.

    Args:
        initialize_lifespan: фикстура, вызывающая lifespan
            без реального запуска приложения.
    """
    async with AsyncClient(app=app, base_url=MAIN_URL) as ac:
        endpoint_ready = '/healthz/ready'
        response = await ac.get(urljoin(MAIN_URL, endpoint_ready))
        assert response.status_code == 200


@pytest.mark.asyncio
@patch('src.app.api.technical_router.db_manager')
async def test_health_check_ready_success(mock_db_connection_success):
    """
    Тестирует эндпоинт /healthz/ready на успешное соединение с базой данных.

    Этот тест проверяет, что при успешном соединении с базой данных
    эндпоинт /healthz/ready возвращает статус 200 OK.

    Args:
        mock_db_connection_success: Мок объекта db_manager,
            используемый для имитации успешного соединения с базой данных.
    """
    fake_connection = AsyncMock()
    fake_connection.fetchval.return_value = 1
    mock_db_connection_success.acquire.return_value.__aenter__.return_value = (
        fake_connection
    )
    mock_db_connection_success.return_value = fake_connection
    async with AsyncClient(app=app, base_url=MAIN_URL) as ac:
        endpoint_ready = '/healthz/ready'
        response = await ac.get(endpoint_ready)
        assert response.status_code == 200


@pytest.mark.asyncio
@patch('src.app.api.technical_router.db_manager')
async def test_health_check_not_ready(mock_db_conn_failure):
    """
    Тестирует эндпоинт /healthz/ready на недоступность базы данных.

    Этот тест проверяет, что при возникновении ошибки соединения с базой данных
    эндпоинт /healthz/ready возвращает статус 500 Internal Server Error.

    Args:
        mock_db_conn_failure: Мок объекта db_manager,
            используемый для имитации сбоя соединения с базой данных.
    """
    mock_db_conn_failure.get_db_connection.side_effect = Exception('DB Error')
    async with AsyncClient(app=app, base_url=MAIN_URL) as ac:
        endpoint_ready = '/healthz/ready'
        response = await ac.get(endpoint_ready)
        assert response.status_code == 500
