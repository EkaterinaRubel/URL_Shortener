"""Модуль является точкой входа для запуска веб-сервиса."""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.app.api.technical_router import router as technical_router
from src.app.config.config_api import HOST, PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Логика определяемая при старте и перед закрытием.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Yields:
        None
    """
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(technical_router)


if __name__ == '__main__':
    uvicorn.run(
        app='src.app.main:app',
        host=HOST,
        port=PORT,
        reload=True,
        http='h11',
    )
