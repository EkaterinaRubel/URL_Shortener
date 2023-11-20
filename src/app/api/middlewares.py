"""Модуль для реализации Middleware."""
import time

from fastapi import Request, Response
from opentracing import (InvalidCarrierException,  # noqa: I001
                         SpanContextCorruptedException,  # noqa: I001, WPS318
                         global_tracer, propagation, tags)  # noqa: I001, WPS319, E501
from prometheus_client import Counter, Gauge, Histogram  # noqa: I005
from starlette.status import HTTP_400_BAD_REQUEST

readiness_probe_gauge = Gauge(
    'rubel_service_readiness',
    'Indicates if the service is ready to handle requests',
)

request_latency_histogram = Histogram(
    'rubel_request_latency',
    'Request latency.',
    ['operation', 'http_status_code', 'error'],
)


async def metrics_middleware(request: Request, call_next):
    """
    Middleware для реализации логгирования времени выполнения запроса.

    Args:
        request (Request): Входящий запрос, который нужно обработать.
        call_next: Следующий слой middleware или конечный обработчик.

    Returns:
        Response: Ответ после выполнения запроса.
    """
    start_time = time.monotonic()
    response: Response = await call_next(request)
    operation = f'{request.method} {request.url.path}'  # noqa: WPS237
    request_latency_histogram.labels(
        operation,
        response.status_code,
        response.status_code >= HTTP_400_BAD_REQUEST,
    ).observe(
        time.monotonic() - start_time,
    )
    return response


requests_count = Counter(
    'rubel_request_total',
    'Count number of requests',
    ['endpoint', 'status_code'],
)


async def collect_metrics(request: Request, call_next):
    """
    Middleware логгирования  кол. запросов в разрезе эндпоинтов и статус кодов.

    Args:
        request (Request): Входящий запрос, который нужно обработать.
        call_next: Следующий слой middleware или конечный обработчик.

    Returns:
        Response: Ответ после выполнения запроса.
    """
    response = await call_next(request)
    requests_count.labels(
        endpoint=request.url.path,
        status_code=response.status_code,
    ).inc()
    return response


async def tracing_middleware(request: Request, call_next):
    """
    Middleware для реализации трейсинга.

    Извлекает информацию о трейсинге из HTTP-заголовков входящего запроса
    и создает корневой спан (span) для дальнейшего трейсинга операций.

    Пропускает трейсинг для эндпоинтов '/health', '/ready', '/metrics'.

    Args:
        request (Request): Входящий запрос, который нужно обработать.
        call_next: Следующий слой middleware или конечный обработчик запроса.

    Returns:
        Response: Ответ после выполнения запроса.
    """
    path = request.url.path
    skiped_endpoints = ['/health', '/ready', '/metrics']
    if any(path.startswith(prefix) for prefix in skiped_endpoints):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS,
            request.headers,
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: request.url,
    }
    with global_tracer().start_active_span(
        str(request.url.path), child_of=span_ctx, tags=span_tags,
    ):
        return await call_next(request)
