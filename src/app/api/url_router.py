"""Модуль обработки и управления URL-адресами."""
import re

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from src.app.api.schemas import LongUrlModel
from src.app.config.config_api import MAIN_URL
from src.data_base.repositories.url_mapping import URLMappingRepository

router = APIRouter()


@router.post('/shorten/')
async def create_short_url(long_url_model: LongUrlModel):
    """
    Генерирует короткий url на основе предоставленного длинного url.

    Args:
        long_url_model (LongUrlModel): Модель для валидации длинных URL.

    Returns:
        JSON: Объект JSON с сокращенным url.
    """
    long_url = str(long_url_model.long_url)
    short_hash = await URLMappingRepository().put_date(long_url)
    return f'{MAIN_URL}/{short_hash}'


@router.get('/{short_url}')
async def read_short_url(short_url: str):
    """
    Получает короткий url и перенаправляет на соответствующий длинный url.

    Args:
        short_url (str): Короткий url.

    Raises:
        HTTPException: если длинный url для переданного короткого не найден.

    Returns:
        RedirectResponse: HTTP-ответ с перенаправлением на длинный url.
    """
    if short_url == 'metrics':
        return None
    if not re.match('^[a-zA-Z0-9]{6}$', short_url):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid short_url',
        )

    long_url = await URLMappingRepository().find_long_url(short_url)
    if long_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(
        long_url,
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
