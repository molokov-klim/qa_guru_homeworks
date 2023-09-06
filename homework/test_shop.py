"""
Тестовый модуль для проверки классов из homework.models
"""
# pylint: disable=import-error, disable=redefined-outer-name
import pytest

from homework.models import Product, Cart
from homework.providers import CsvProductProvider, ProductProvider


@pytest.fixture(params=[CsvProductProvider])
def provider(request) -> ProductProvider:
    """
    Pytest фикстура, возвращающая экземпляр ProductProvider.

    Эта фикстура параметризуется различными реализациями ProductProvider.
    На данный момент используется только `CsvProductProvider`,
    но в будущем в список `params` можно добавить
    другие реализации провайдеров.

    Args:
     request: объект запроса pytest, который предоставляет доступ к текущему используемому параметру
     (в данном случае, типу ProductProvider).
    Returns:
        Экземпляр текущей реализации ProductProvider.
    """
    return request.param()


@pytest.fixture
def products(provider) -> list[Product]:
    """
    Pytest фикстура, возвращающая список продуктов, полученных от поставщика.
    Использует другую фикстуру `provider` для получения экземпляра provider и
    вызывает его метод `get_products`.

    Args:
        provider: Экземпляр поставщика продуктов (ProductProvider).

    Returns:
        Список продуктов (list[Product]).
    """
    product_list = provider.get_products()
    return product_list


@pytest.fixture(params=[Cart])
def cart(request) -> Cart:
    """
    Pytest фикстура, возвращающая экземпляр корзины для покупок.

    Эта фикстура параметризуется различными реализациями корзины.
    На данный момент используется только `Cart`, но в будущем в список `params` можно добавить
    другие реализации корзин.

    Args:
        request: объект запроса pytest, который предоставляет доступ к
        текущему используемому параметру
        (в данном случае, типу Cart).

    Returns:
        Экземпляр текущей реализации корзины (Cart).
    """
    return request.param()


class TestProducts:
    check_quantity_positive_modifiers = (0, -1, -50, -100)
    check_quantity_negative_modifiers = (1000, 50000, 500000, 1000000)
    buy_positive_modifiers = (-1, -5, -100)

    @pytest.mark.parametrize("modifier", check_quantity_positive_modifiers)
    def test_product_check_quantity_positive(self, modifier, products):
        item = products[self.check_quantity_positive_modifiers.index(modifier)]
        assert item.check_quantity(quantity=item.quantity + modifier)

    @pytest.mark.xfail
    @pytest.mark.parametrize("modifier", check_quantity_negative_modifiers)
    def test_product_check_quantity_negative(self, products, modifier):
        item = products[self.check_quantity_negative_modifiers.index(modifier)]
        assert item.check_quantity(quantity=item.quantity + modifier)

    @pytest.mark.parametrize("modifier", buy_positive_modifiers)
    def test_product_buy_positive(self, products, modifier):
        item = products[self.buy_positive_modifiers.index(modifier)]
        before_quantity = item.quantity
        item.buy(quantity=item.quantity + modifier)
        after_quantity = item.quantity
        assert before_quantity > after_quantity, f"{item=}, {before_quantity=}, {after_quantity=}"
        item.quantity = before_quantity

    # @pytest.mark.xfail
    @pytest.mark.parametrize("modifier", check_quantity_negative_modifiers)
    def test_product_buy_negative_more_than_available(self, products, modifier):
        item = products[self.check_quantity_negative_modifiers.index(modifier)]
        before_quantity = item.quantity
        with pytest.raises(ValueError):
            item.buy(quantity=item.quantity + modifier)
        item.quantity = before_quantity


class TestCart:
    add_product_positive_modifiers = (1, 100, 99999)
    add_product_negative_modifiers = (0, -1, -100, -99999)

    @pytest.mark.parametrize("modifier", add_product_positive_modifiers)
    def test_add_product_positive(self, cart, products, modifier):
        item = products[0]
        cart.add_product(product=item, buy_count=modifier)
        before_quantity = cart.products[item]
        cart.add_product(product=item, buy_count=modifier)
        after_quantity = cart.products[item]
        assert before_quantity < after_quantity

    @pytest.mark.parametrize("modifier", add_product_negative_modifiers)
    def test_add_product_negative(self, cart, products, modifier):
        item = products[0]
        with pytest.raises(ValueError):
            cart.add_product(product=item, buy_count=modifier)

    def test_remove_product(self, cart, products):
        item = products[0]
        cart.add_product(product=item, buy_count=3)
        cart.remove_product(product=item, remove_count=1)
        assert cart.products[item] == 2

    def test_remove_product_more_than_have(self, cart, products):
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.remove_product(product=item, remove_count=2)
        assert cart.products == {}

    def test_remove_product_without_count(self, cart, products):
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.remove_product(product=item)
        assert cart.products == {}

    def test_clear(self, cart, products):
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, cart, products):
        item = products[0]
        cart.add_product(product=item, buy_count=3)
        assert cart.get_total_price() == 300.0

    def test_buy_positive(self, cart, products):
        item = products[0]
        quantity = item.quantity
        cart.add_product(product=item, buy_count=quantity)
        cart.buy()
        assert cart.get_total_price() == 0
        item.quantity = quantity

    def test_buy_negative(self, cart, products):
        item = products[0]
        quantity = item.quantity + 1
        cart.add_product(product=item, buy_count=quantity)
        with pytest.raises(ValueError):
            cart.buy()

    def test_process_payment(self, cart, products):
        item = products[0]
        quantity = item.quantity
        cart.add_product(product=item, buy_count=quantity)
        assert cart.process_payment() is True
