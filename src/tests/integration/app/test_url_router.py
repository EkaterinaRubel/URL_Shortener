"""Модуль тестирования endpoints обработки url."""
from urllib.parse import urljoin

import pytest
from httpx import AsyncClient

from src.app.config.config_api import MAIN_URL
from src.app.logic.generators_short_url import generate_short_url
from src.app.main import app


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'long_url, expected_value',
    [
        pytest.param(
            'https://www.example.com',
            f'{MAIN_URL}/{generate_short_url("https://www.example.com/")}',
            id='test_create_short_url',
        ),
        pytest.param(
            'http://www.testing.com',
            f'{MAIN_URL}/{generate_short_url("http://www.testing.com/")}',
            id='test_return_created_short_url',
        ),
    ],
)
async def test_shorten(
    long_url,
    expected_value,
    put_url_map,
):
    """
    Тестирует функционал создания короткой ссылки.

    Проверяет, что API возвращает корректный статус и короткую ссылку
    для заданного длинного URL.

    Args:
        long_url (str): Исходный длинный URL.
        expected_value (str): Ожидаемое значение короткой ссылки.
        put_url_map (fixture): Фикстура для подготовки данных.

    Asserts:
        Проверяет, что возвращаемое значение соответствует ожидаемому.
    """
    async with AsyncClient(app=app, base_url=MAIN_URL) as ac:
        endpoint_shorten = '/shorten/'
        response = await ac.post(
            urljoin(MAIN_URL, endpoint_shorten),
            json={'long_url': long_url},
        )
        assert response.json() == expected_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'short_url, expected_status, expected_header',
    [
        pytest.param(
            generate_short_url('http://www.testing.com/'),
            301,
            'http://www.testing.com/',
            id='test_read_short_url',
        ),
        pytest.param(
            'fake00',
            404,
            None,
            id='test_read_nonexistent_short_url',
        ),
        pytest.param(
            'Invalid',
            404,
            None,
            id='test_read_invalid_short_url',
        ),
    ],
)
async def test_read(
    short_url,
    expected_status,
    expected_header,
    put_url_map,
):
    """
    Тестирует функционал перехода по короткой ссылке.

    Проверяет, что API возвращает корректный статус ответа и,
    при необходимости, правильный заголовок 'Location' для перенаправления.

    Args:
        short_url (str): Короткая ссылка для тестирования.
        expected_status (int): Ожидаемый HTTP статус ответа.
        expected_header (str): Ожидаемое значение заголовка 'Location'.
        put_url_map (fixture): Фикстура для подготовки данных.

    Asserts:
        Проверяет, что статус ответа соответствует ожидаемому и,
        если применимо, что заголовок 'Location' соответствует
        oжидаемому значению.
    """
    async with AsyncClient(app=app, base_url=MAIN_URL) as ac:
        response = await ac.get(urljoin(MAIN_URL, short_url))
        assert response.status_code == expected_status
        if expected_header:
            assert response.headers['Location'] == expected_header
