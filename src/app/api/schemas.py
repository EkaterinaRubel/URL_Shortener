"""Схемы моделей валидации данных."""
from pydantic import BaseModel, HttpUrl


class LongUrlModel(BaseModel):
    """Модель для валидации длинных URL."""

    long_url: HttpUrl
