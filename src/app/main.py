"""Модуль является точкой входа для запуска веб-сервиса."""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from starlette.middleware.base import BaseHTTPMiddleware

from src.app.api.middlewares import collect_metrics, metrics_middleware, tracing_middleware  # noqa: I001, E501
from src.app.api.technical_router import router as technical_router
from src.app.api.url_router import router as url_router
from src.app.config.config_api import HOST, PORT, config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Логика определяемая при старте и перед закрытием.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Yields:
        jaeger_tracer
    """
    tracer = config.initialize_tracer()
    yield {'jaeger_tracer': tracer}

app = FastAPI(lifespan=lifespan)
app.include_router(technical_router)
app.include_router(url_router)

metrics_app = make_asgi_app()
app.mount('/metrics/', metrics_app)
app.add_middleware(BaseHTTPMiddleware, dispatch=metrics_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=collect_metrics)
app.add_middleware(BaseHTTPMiddleware, dispatch=tracing_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(
        app='src.app.main:app',
        host=HOST,
        port=PORT,
        reload=True,
        http='h11',
    )
