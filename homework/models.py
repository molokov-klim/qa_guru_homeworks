"""
Модуль для управления продуктами и корзиной покупок.
"""
from typing import cast


class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    _instances = {}  # словарь для хранения экземпляров

    def __new__(cls, name: str, price: float, description: str, quantity: int):
        temp_instance = super().__new__(cls)
        temp_instance.name = name
        temp_instance.price = price
        temp_instance.description = description
        temp_instance.quantity = quantity

        key = temp_instance.__hash__()

        if key in cls._instances:
            return cls._instances[key]

        cls._instances[key] = temp_instance
        return temp_instance

    def __init__(self, name: str, price: float, description: str, quantity: int):
        if self.__hash__() not in Product._instances:
            self.name = name
            self.price = price
            self.description = description
            self.quantity = quantity

    def __hash__(self):
        return hash(self.name + self.description)

    def __str__(self):
        return f"Product('{self.name=}', {self.price=}, '{self.description=}', {self.quantity=})"

    def __repr__(self):
        return f"Product('{self.name=}', {self.price=}, '{self.description=}', {self.quantity=})"

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.name == other.name and self.description == other.description
        return False

    def check_quantity(self, quantity: int) -> bool:
        """
        Метод проверки наличия запрашиваемого количество товара на складе.
        Args:
            quantity (int): запрашиваемое количество товара
        Returns:
            True если количество продукта больше или равно запрашиваемому,
            False в ином случае
        """
        if self.quantity >= quantity:
            return True
        return False

    def buy(self, quantity: int) -> 'Product':
        """
        Метод покупки товара.

        Args:
            quantity (int): покупаемое количество товара
        Returns:
            self
        Raises:
            ValueError, если количество товара на складе недостаточно
        """
        if not self.check_quantity(quantity):
            raise ValueError("Невозможно совершить покупку. Товара на складе недостаточно")
        self.quantity -= quantity
        return cast('Product', self)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def __str__(self):
        return f"Cart('{self.products=}') # item: quantity"

    def __repr__(self):
        return f"Cart('{self.products=}') # item: quantity"

    def add_product(self, product: Product, buy_count: int = 1) -> 'Cart':
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличивает количество.

        Args:
            product (Product): добавляемый товар.
            buy_count (int): количество добавляемого товара.
        Returns:
            self
        """

        if buy_count <= 0:
            raise ValueError("Некорректное количество товара")
        if product in self.products:
            self.products[product] += buy_count
            return cast('Cart', self)

        self.products[product] = buy_count
        return cast('Cart', self)

    def remove_product(self, product: Product, remove_count: int = None) -> 'Cart':
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        Args:
            product (Product): удаляемый товар.
            remove_count (int): количество удаляемого товара.
        Returns:
            self
        """
        if product not in self.products:
            return cast('Cart', self)
        if remove_count is None or remove_count >= self.products[product]:
            del self.products[product]
        else:
            self.products[product] -= remove_count
        return cast('Cart', self)

    def clear(self) -> 'Cart':
        """
        Метод очистки корзины.
        Returns:
            self
        """
        self.products.clear()
        return cast('Cart', self)

    def get_total_price(self) -> float:
        """
        Метод получения суммы стоимостей товаров в корзине.
        Returns:
            float - сумма стоимостей товаров
        """
        amount = 0
        for product, quantity in self.products.items():
            amount += product.price * quantity
        return amount

    def buy(self) -> 'Cart':
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError

        Returns:
            self
        """
        for product, quantity in self.products.items():
            if not product.check_quantity(quantity):
                raise ValueError(f"Товара {product} недостаточно на складе. Остаток: {quantity}")
        assert self.process_payment()
        for product, quantity in self.products.items():
            product.buy(quantity)
        self.clear()
        return cast('Cart', self)

    def process_payment(self) -> bool:
        """
        Заглушка для метода проведения оплаты.
        Returns:
            True
        """
        self.get_total_price()
        # payment mock
        return True
