"""Модуль предоставляет методы для работы с таблицей url_mapping в БД."""
from src.app.logic.generators_short_url import generate_short_url
from src.data_base.connections.connections import db_manager


class URLMappingRepository(object):
    """Предоставляет методы для работы c хранилищем пар url."""

    async def put_date(self, long_url: str):
        """
        Метод вставляет новую пару короткий:длинный url.

        Предварительно выполняется проверка наличия
        длинного url в БД.

        Args:
            long_url (str): длинный url

        Returns:
            str: короткий url
        """
        short_url = await self._check_long_url_in_db(long_url)
        if short_url:
            return short_url

        short_url = generate_short_url(long_url)
        async with db_manager.get_db_connection() as connection:
            query_insert = """
            INSERT INTO url_mapping (short_url, long_url) VALUES ($1, $2)
            """
            await connection.execute(query_insert, short_url, long_url)
            return short_url

    async def find_long_url(self, short_url: str):
        """
        Метод возвращает длинный url, соответствующий короткому.

        Args:
            short_url (str): короткий url

        Returns:
            str: длинный url
        """
        async with db_manager.get_db_connection() as connection:
            query_insert = """
            SELECT long_url FROM url_mapping WHERE short_url = $1
            """
            finded_long_url = await connection.fetchval(
                query_insert,
                short_url,
            )
            if finded_long_url:
                await connection.execute(
                    'UPDATE url_mapping SET click_count = click_count + 1 '
                    'WHERE short_url = $1',  # noqa: WPS326
                    short_url,
                )
            return finded_long_url

    async def _check_long_url_in_db(self, long_url: str):
        """
        Проверка наличия длинного url в БД.

        Args:
            long_url (str): Длинный URL для проверки.

        Returns:
            str or None: Возвращает короткий URL, если он найден, иначе None.
        """
        async with db_manager.get_db_connection() as connection:
            query = 'SELECT short_url FROM url_mapping WHERE long_url = $1'
            record = await connection.fetchrow(query, long_url)
            if record:
                return record['short_url']
            return None
