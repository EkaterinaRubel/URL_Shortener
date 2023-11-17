"""Модуль содержит технические эндпоинты проверки здоровья сервиса."""
from fastapi import APIRouter, Response, status

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

    Эндпоинт следует расширить при появлении зависимостей.

    Returns:
        Response: Пустой HTTP-ответ со статус-кодом 200 OK.
    """
    return Response(status_code=status.HTTP_200_OK)
