"""Модуль конфигурации тестовых данных."""

from src.app.logic.generators_short_url import generate_short_url

LONG_URL = 'http://www.testing.com/'
SHORTED_URL = generate_short_url('http://www.testing.com/')
