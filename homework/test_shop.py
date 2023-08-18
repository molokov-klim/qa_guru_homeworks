"""
Протестируйте классы из модуля homework/models.py
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
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
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
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    add_product_positive_modifiers = (1, 100, 99999)
    add_product_negative_modifiers = (0, -1, -100, -99999)

    @pytest.mark.parametrize("modifier", add_product_positive_modifiers)
    def test_add_product_positive(self, cart, products, modifier):
        """
        if buy_count < 0:
            raise ValueError("Некорректное количество товара")
        if product.__hash__() in self.products:
            self.products[product] += buy_count
            return cast('Cart', self)
        self.products[product] = buy_count
        return cast('Cart', self)
        :return:
        """
        item = products[0]
        cart.add_product(product=item, buy_count=modifier)
        before_quantity = cart.products[item]
        cart.add_product(product=item, buy_count=modifier)
        after_quantity = cart.products[item]
        assert before_quantity < after_quantity

    @pytest.mark.parametrize("modifier", add_product_negative_modifiers)
    def test_add_product_negative(self, cart, products, modifier):
        """
        if buy_count < 0:
            raise ValueError("Некорректное количество товара")
        if product.__hash__() in self.products:
            self.products[product] += buy_count
            return cast('Cart', self)
        self.products[product] = buy_count
        return cast('Cart', self)
        :return:
        """
        item = products[0]
        with pytest.raises(ValueError):
            cart.add_product(product=item, buy_count=modifier)
        with pytest.raises(ValueError):
            cart.add_product(product=item, buy_count=modifier)

    def test_remove_product_negative(self, cart, products):
        """
        if product not in self.products:
            return cast('Cart', self)
        if remove_count is None or remove_count >= self.products[product]:
            del self.products[product]
        else:
            self.products[product] -= remove_count
        return cast('Cart', self)
        """
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.remove_product(product=item, remove_count=1)
        with pytest.raises(KeyError):
            assert cart.products[item] == 0

    def test_clear(self, cart, products):
        """
        self.products.clear()
        return cast('Cart', self)
        """
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.clear()
        with pytest.raises(KeyError):
            assert cart.products[item] == 0

    def test_get_total_price(self, cart, products):
        """
        amount = 0
        for product, quantity in self.products.items():
            amount += product.price * quantity
        return amount
        """
        ...

    def test_buy(self, cart, products):
        """
        for product, quantity in self.products.items():
            if not product.check_quantity(quantity):
                raise ValueError(f"Товара {product} недостаточно на складе. Остаток: {quantity}")
        assert self.process_payment()
        for product, quantity in self.products.items():
            product.buy(quantity)
        self.clear()
        return cast('Cart', self)
        """
        ...

    def test_process_payment(self, cart, products):
        """
        amount = self.get_total_price()
        # payment mock
        return True
        """
        ...
