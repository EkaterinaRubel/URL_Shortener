"""Схема таблицы url_mapping."""
from sqlalchemy import BigInteger, Column, DateTime, Sequence, String
from sqlalchemy.sql import func

from src.data_base.models.base import Base


class URLMappingAlchemyModel(Base):
    """
    Модель для представлени структуры таблицы 'url_mapping' в базе данных.

    Attributes:
        url_id (BigInteger): Уникальный идентификатор URL, первичный ключ.
        short_url (String): Сокращенный URL, уникальный и индексированный.
        long_url (String): Длинный URL, не может быть пустым.
        creation_date (DateTime): Дата и время создания записи.
        click_count (BigInteger): Количество переходов по сокращенному URL.
    """

    __tablename__ = 'url_mapping'
    url_id = Column(BigInteger, Sequence('url_id_seq'), primary_key=True)
    short_url = Column(String, unique=True, index=True, nullable=False)
    long_url = Column(String, nullable=False)
    creation_date = Column(DateTime, server_default=func.now())
    click_count = Column(BigInteger, server_default='0', nullable=False)
