"""Модуль выполняющий кодирование длинной ссылки в короткую."""
import hashlib


def generate_short_url(long_url: str) -> str:
    """
    Генерирует короткий URL от длинного на основе хеша MD5.

    Args:
        long_url (str): Исходный URL.

    Returns:
        str: Сокращенный URL, представляющий собой первые 6 символов хеша MD5.
    """
    md5_hasher = hashlib.md5()  # noqa: S324
    md5_hasher.update(long_url.encode('utf-8'))
    return md5_hasher.hexdigest()[:6]
