"""Модуль содержит технические эндпоинты проверки здоровья сервиса."""
from fastapi import APIRouter, Response, status

from src.app.api.middlewares import readiness_probe_gauge

router = APIRouter()

readiness_probe_gauge.set(0)


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

    Эндпоинт следует расширить при появлении зависимостей.

    Returns:
        Response: Пустой HTTP-ответ со статус-кодом 200 OK.
    """
    readiness_probe_gauge.set(1)
    return Response(status_code=status.HTTP_200_OK)
