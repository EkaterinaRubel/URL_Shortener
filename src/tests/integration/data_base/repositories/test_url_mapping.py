"""Модуль тестирования класса URLMappingRepository."""
import pytest

from src.app.logic.generators_short_url import generate_short_url
from src.data_base.repositories.url_mapping import URLMappingRepository
from src.tests.tests_config import LONG_URL, SHORTED_URL


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'input_url, expected_value',
    [
        pytest.param(
            'https://www.2example.com',
            generate_short_url('https://www.2example.com'),
            id='test_put_date',
        ),
        pytest.param(
            LONG_URL,
            SHORTED_URL,
            id='test_put_created_date',
        ),
    ],
)
async def test_put_date(
    input_url,
    expected_value,
    put_url_map,
):
    """
    Тестирует функционал создания короткой ссылки.

    Проверяет, что метод put_date возвращает ожидаемое значение
    для заданного длинного URL.

    Args:
        input_url (str): Исходный длинный URL.
        expected_value (str): Ожидаемое значение короткой ссылки.
        put_url_map (fixture): Фикстура для подготовки данных.

    Asserts:
        Проверяет, что возвращаемое значение соответствует ожидаемому.
    """
    rep = URLMappingRepository()
    current_value = await rep.put_date(input_url)
    assert current_value == expected_value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'input_url, expected_value',
    [
        pytest.param(
            SHORTED_URL,
            LONG_URL,
            id='test_find_long_url',
        ),
        pytest.param(
            'fake00',
            None,
            id='test_find_nonexistent_long_url',
        ),
    ],
)
async def test_find_long_url(
    input_url,
    expected_value,
    put_url_map,
):
    """
    Тестирует функционал поиска исходного длинного URL по короткой ссылке.

    Проверяет, что метод find_long_url возвращает ожидаемое значение
    для заданной короткой ссылки.

    Args:
        input_url (str): Короткая ссылка для тестирования.
        expected_value (str or None): Ожидаемый исходный длинный URL или None.
        put_url_map (fixture): Фикстура для подготовки данных.

    Asserts:
        Проверяет, что возвращаемое значение соответствует ожидаемому.
    """
    rep = URLMappingRepository()
    current_value = await rep.find_long_url(input_url)
    assert current_value == expected_value
