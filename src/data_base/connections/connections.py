"""Модуль предоставляет методы управления соединением с БД."""
from contextlib import asynccontextmanager

import asyncpg

from src.data_base.config.config import app_config


class DBManager(object):
    """
    Класс для управления пулом соединений с базой данных.

    Предоставляет методы для создания и закрытия пула соединений,
    а также для получения и освобождения соединений из пула.
    """

    async def create_pool(self):
        """Создает пул соединений с базой данных."""
        self.pool = await asyncpg.create_pool(
            f'postgresql://{app_config.postgres.url}',  # noqa: WPS237
        )

    async def close_pool(self):
        """Закрывает пул соединений с базой данных."""
        await self.pool.close()

    @asynccontextmanager
    async def get_db_connection(self):
        """
        Получает асинхронное соединение с БД из пула.

        Контекстный менеджер освобождает соединение после использования.

        Yields:
            asyncpg.Connection: Асинхронное соединение с базой данных.
        """
        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)


db_manager = DBManager()
