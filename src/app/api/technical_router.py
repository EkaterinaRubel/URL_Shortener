"""Модуль содержит технические эндпоинты проверки здоровья сервиса."""
from fastapi import APIRouter, Response, status

from src.app.api.middlewares import readiness_probe_gauge
from src.data_base.connections.connections import db_manager

router = APIRouter()


@router.get('/healthz/up')
async def health_check_up():
    """
    Проверка работы сервиса.

    Returns:
        Response: Пустой HTTP-ответ со статус-кодом 200 OK.
    """
    return Response(status_code=status.HTTP_200_OK)


@router.get('/healthz/ready')
async def health_check_ready():
    """
    Проверка готовности сервиса.

    Проверяет доступность базы данных.

    Returns:
        Response: Пустой HTTP-ответ со статус-кодом 200 OK.
    """
    try:  # noqa: WPS229
        async with db_manager.get_db_connection() as connection:
            await connection.fetchval('SELECT 1')
        readiness_probe_gauge.set(1)
        return Response(status_code=status.HTTP_200_OK)
    except Exception:
        readiness_probe_gauge.set(0)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
