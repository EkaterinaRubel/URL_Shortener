"""Модуль предоставляет методы для работы c хранилищем пар url."""
from src.app.logic.generators_short_url import generate_short_url


class URLMappingRepository(object):
    """Предоставляет методы для работы c хранилищем пар url."""

    url_mapping = {generate_short_url('http://www.testing.com/'): 'http://www.testing.com/'}  # noqa: E501

    _instance = None

    def __new__(cls):
        """Паттерн Singleton."""  # noqa: DAR201
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def put_date(self, long_url: str):
        """
        Метод вставляет новую пару короткий:длинный url.

        Предварительно выполняется проверка наличия
        длинного url.

        Args:
            long_url (str): длинный url

        Returns:
            str: короткий url
        """
        existing_short_url = [
            key for key, exist_url in self.url_mapping.items() if exist_url == long_url  # noqa: E501
        ]
        if existing_short_url:
            return {'short_url': existing_short_url[0]}
        short_url = generate_short_url(long_url)
        self.url_mapping[short_url] = long_url
        return short_url

    async def find_long_url(self, short_url: str):
        """
        Метод возвращает длинный url, соответствующий короткому.

        Args:
            short_url (str): короткий url

        Returns:
            str: длинный url
        """
        return self.url_mapping.get(short_url, None)
