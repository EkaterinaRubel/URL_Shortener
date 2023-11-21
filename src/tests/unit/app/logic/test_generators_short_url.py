"""Модуль тестирования функционала генерации коротких URL."""
from src.app.logic.generators_short_url import generate_short_url


def test_generate_short_url_length():
    """Длина короткого URL соответствует ожидаемой."""
    long_url = 'http://www.example.com'
    short_url = generate_short_url(long_url)
    assert len(short_url) == 6


def test_generate_short_url_consistency():
    """Для одинаковых исходных URL генерируется одинаковый короткий URL."""
    long_url1 = 'http://www.example.com'
    long_url2 = 'http://www.example.com'
    assert generate_short_url(long_url1) == generate_short_url(long_url2)


def test_generate_short_url_uniqueness():
    """Для разных исходных URL генерируются уникальные короткие URL."""
    long_url1 = 'http://www.example1.com'
    long_url2 = 'http://www.example2.com'
    assert generate_short_url(long_url1) != generate_short_url(long_url2)
