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
    """
    Тесты на класс Product
    """
    check_quantity_positive_modifiers = (0, -1, -50)
    check_quantity_negative_modifiers = (1, 50)

    @pytest.mark.parametrize("modifier", check_quantity_positive_modifiers)
    def test_product_check_quantity_positive(self, products, modifier):
        """
        Проверяет, что метод check_quantity корректно реагирует на положительные
        изменения в количестве товара.

        Тест параметризован модификаторами, которые добавляются к текущему количеству товара.
        Ожидается, что метод check_quantity будет возвращать True для всех этих комбинаций.

        Args:
            products (list[Product]): Список продуктов для проверки.
            modifier (int): Значение, которое будет добавлено к текущему количеству товара.

        """
        for item in products:
            assert item.check_quantity(quantity=item.quantity + modifier)

    @pytest.mark.xfail
    @pytest.mark.parametrize("modifier", check_quantity_negative_modifiers)
    def test_product_check_quantity_negative(self, products, modifier):
        """
        Проверяет, что метод check_quantity корректно реагирует на отрицательные
        изменения в количестве товара.

        Тест параметризован модификаторами, которые добавляются к текущему количеству товара.
        Поскольку этот тест помечен как xfail, ожидается его неудачное завершение.

        Args:
            products (list[Product]): Список продуктов для проверки.
            modifier (int): Значение, которое будет добавлено к текущему количеству товара.

        """
        for item in products:
            assert item.check_quantity(quantity=item.quantity + modifier)

    @pytest.mark.parametrize("modifier", check_quantity_positive_modifiers)
    def test_product_buy_positive(self, products, modifier):
        """
        Проводит покупку и проверяет, что количество продукта после покупки уменьшилось.
        Тест параметризован модификаторами, которые добавляются к текущему
        количеству товара для покупки.
        После выполнения покупки, количество товара восстанавливается в исходное значение.

        Args:
            products (list[Product]): Список продуктов для проверки.
            modifier (int): Значение, которое будет добавлено к текущему количеству
            товара для покупки.

        """
        for item in products:
            before_quantity = item.quantity
            item.buy(quantity=item.quantity + modifier)
            after_quantity = item.quantity
            assert before_quantity > after_quantity, \
                f"{item=}, {before_quantity=}, {after_quantity=}"
            item.quantity = before_quantity

    # @pytest.mark.xfail
    @pytest.mark.parametrize("modifier", check_quantity_negative_modifiers)
    def test_product_buy_negative_more_than_available(self, products, modifier):
        """
        Проверяет, что при попытке купить товар в количестве, превышающем доступное,
        будет выброшено исключение ValueError. Тест параметризован модификаторами,
        которые добавляются к текущему количеству товара для покупки. После каждой проверки,
        количество товара восстанавливается в исходное значение.

        Args:
            products (list[Product]): Список продуктов для проверки.
            modifier (int): Значение, которое будет добавлено к текущему
            количеству товара для покупки.

        """
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
        """
        Проверяет, что после добавления продукта в корзину его
        количество увеличивается.
        Тест параметризован положительными модификаторами, указывающими сколько
        единиц товара нужно добавить.
        В ходе теста товар добавляется в корзину дважды, и проверяется, что его
        количество в корзине увеличивается.

        Args:
            cart (Cart): Экземпляр корзины для покупок.
            products (list[Product]): Список продуктов, из которого будет
            выбран первый товар для добавления в корзину.
            modifier (int): Количество единиц товара, которое нужно добавить в корзину.

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
        Тест ожидает, что при попытке добавить в корзину товар с отрицательным количеством
        или нулевым количеством будет выброшено исключение ValueError. Тест параметризован
        отрицательными модификаторами, указывающими сколько единиц товара добавить.

        Args:
            cart (Cart): Экземпляр корзины для покупок.
            products (list[Product]): Список продуктов, из которого
            будет выбран первый товар для добавления в корзину.
            modifier (int): Количество единиц товара, которое пытаются добавить в корзину.

        """
        item = products[0]
        with pytest.raises(ValueError):
            cart.add_product(product=item, buy_count=modifier)

    def test_remove_product_negative(self, cart, products):
        """
        Проверяет реакцию корзины при попытке доступа к удаленному продукту.

        В ходе теста продукт добавляется в корзину, затем удаляется из неё. После этого ожидается,
        что попытка обратиться к этому продукту в корзине вызовет исключение KeyError.
        Таким образом, тест проверяет корректность удаления продукта из корзины.

        Args:
            cart (Cart): Экземпляр корзины для покупок.
            products (list[Product]): Список продуктов, из которого будет выбран первый товар для
            добавления и последующего удаления из корзины.
        """
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.remove_product(product=item, remove_count=1)
        with pytest.raises(KeyError):
            assert cart.products[item] == 0

    def test_clear(self, cart, products):
        """
        Проверяет функционал очистки корзины от всех продуктов.

        В ходе теста продукт добавляется в корзину, после чего корзина полностью
        очищается с использованием метода `clear`.
        Ожидается, что после очистки попытка обратиться к ранее добавленному
        продукту в корзине вызовет исключение KeyError.
        Тест проверяет, что метод `clear` корректно удаляет все продукты из корзины.

        Args:
            cart (Cart): Экземпляр корзины для покупок.
            products (list[Product]): Список продуктов, из которого будет выбран
            первый товар для добавления в корзину и проверки после очистки.

        """
        item = products[0]
        cart.add_product(product=item, buy_count=1)
        cart.clear()
        with pytest.raises(KeyError):
            assert cart.products[item] == 0

    def test_get_total_price(self, cart, products):
        """
        Проверяет корректность расчета общей стоимости продуктов в корзине.

        В ходе теста продукт добавляется в корзину в количестве 3 единиц.
        Затем проверяется, что метод `get_total_price` корректно рассчитывает общую
        стоимость продуктов в корзине.
        Предполагается, что стоимость одной единицы товара равна 100.0,
        следовательно, общая стоимость трех единиц будет 300.0.

        Args:
            cart (Cart): Экземпляр корзины для покупок.
            products (list[Product]): Список продуктов, из которого будет выбран
            первый товар для добавления в корзину и расчета стоимости.

        """
        item = products[0]
        cart.add_product(product=item, buy_count=3)
        assert cart.get_total_price() == 300.0

    def test_buy_positive(self, cart, products):
        """
        Проверяет корректность покупки всех продуктов в корзине.

        В этом тесте продукт добавляется в корзину в количестве, равном его текущему запасу.
        После этого происходит покупка всех товаров в корзине с использованием метода `buy`.
        Ожидается, что после покупки общая стоимость продуктов в корзине будет равна 0,
        так как корзина должна быть пуста. В конце теста
        количество товара восстанавливается, чтобы не влиять на последующие тесты.

        Args:
            cart (Cart): Экземпляр корзины для покупок.
            products (list[Product]): Список продуктов, из которого будет выбран первый товар
            для добавления в корзину, покупки и восстановления количества.

        """
        item = products[0]
        quantity = item.quantity
        cart.add_product(product=item, buy_count=quantity)
        cart.buy()
        assert cart.get_total_price() == 0
        item.quantity = quantity

    def test_buy_negative(self, cart, products):
        """
        Проверяет реакцию корзины при попытке купить количество продукта больше, чем доступно.

        В этом тесте продукт добавляется в корзину в количестве, превышающем его текущий запас на 1.
        Затем тест ожидает, что попытка купить все товары в корзине с использованием метода `buy`
        вызовет исключение ValueError, так как количество товара для покупки превышает
        доступное количество.

        Args:
            cart (Cart): Экземпляр корзины для покупок.
            products (list[Product]): Список продуктов, из которого будет выбран первый товар для
            добавления в корзину и попытки покупки.

        """
        item = products[0]
        quantity = item.quantity + 1
        cart.add_product(product=item, buy_count=quantity)
        with pytest.raises(ValueError):
            cart.buy()

    def test_process_payment(self, cart, products):
        """
        Проверяет корректность обработки платежа после добавления продуктов в корзину.

        В этом тесте продукт добавляется в корзину в количестве, равном его текущему запасу.
        Затем тест ожидает, что метод `process_payment` корректно обработает платеж и вернет `True`
        как индикатор успешного завершения операции.

        Args:
            cart (Cart): Экземпляр корзины для покупок.
            products (list[Product]): Список продуктов, из которого будет выбран первый товар для
            добавления в корзину и последующей обработки платежа.

        """
        item = products[0]
        quantity = item.quantity
        cart.add_product(product=item, buy_count=quantity)
        assert cart.process_payment() is True
