"""
Тестовый модуль для проверки классов из homework.models
"""

import pytest

from homework.models import Product, Cart
from homework.providers import CsvProductProvider, ProductProvider


@pytest.fixture(params=[CsvProductProvider])
def provider(request) -> ProductProvider:
    return request.param()


@pytest.fixture
def products(provider) -> list[Product]:
    product_list = provider.get_products()
    return product_list


@pytest.fixture(params=[Cart])
def cart(request) -> Cart:
    return request.param()


class TestProducts:
    """
    Тесты на класс Product
    """
    check_quantity_positive_modifiers = (0, -1, -50)
    check_quantity_negative_modifiers = (1, 50)

    @pytest.mark.parametrize("modifier", check_quantity_positive_modifiers)
    def test_product_check_quantity_positive(self, products, modifier):
        for item in products:
            assert item.check_quantity(quantity=item.quantity + modifier)

    @pytest.mark.xfail
    @pytest.mark.parametrize("modifier", check_quantity_negative_modifiers)
    def test_product_check_quantity_negative(self, products, modifier):
        for item in products:
            assert item.check_quantity(quantity=item.quantity + modifier)

    @pytest.mark.parametrize("modifier", check_quantity_positive_modifiers)
    def test_product_buy_positive(self, products, modifier):
        for item in products:
            before_quantity = item.quantity
            item.buy(quantity=item.quantity + modifier)
            after_quantity = item.quantity
            assert before_quantity > after_quantity, f"{item=}, {before_quantity=}, {after_quantity=}"
            item.quantity = before_quantity

    # @pytest.mark.xfail
    @pytest.mark.parametrize("modifier", check_quantity_negative_modifiers)
    def test_product_buy_negative_more_than_available(self, products, modifier):
        for item in products:
            before_quantity = item.quantity
            with pytest.raises(ValueError):
                item.buy(quantity=item.quantity + modifier)
            item.quantity = before_quantity


class TestCart:
    """
    Тесты на класс Cart
    """
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
        with pytest.raises(ValueError):
            cart.add_product(product=item, buy_count=modifier)

    def test_remove_product_negative(self, cart, products):
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.remove_product(product=item, remove_count=1)
        with pytest.raises(KeyError):
            assert cart.products[item] == 0

    def test_clear(self, cart, products):
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.clear()
        with pytest.raises(KeyError):
            assert cart.products[item] == 0

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
