"""
Протестируйте классы из модуля homework/models.py
"""

import pytest

from homework.models import Product
from homework.providers import CsvProductProvider, DatabaseProductProvider, ApiProductProvider, ProductProvider


@pytest.fixture(params=[CsvProductProvider, DatabaseProductProvider, ApiProductProvider])
def provider(request) -> ProductProvider:
    return request.param()


@pytest.fixture
def product(provider) -> list[Product]:
    return provider.get_products()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        pass

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        pass

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        pass


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
