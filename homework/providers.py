"""
Модуль управляющий доступом к источникам данных
"""
import warnings
from abc import ABC, abstractmethod
import logging
import csv

from homework.models import Product


# pylint: disable=too-few-public-methods
class ProductProvider(ABC):
    """
    Абстрактный класс доступа к данным
    """

    def __init__(self, logger: logging.Logger = None):
        if logger is None:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        self.logger = logger

    @abstractmethod
    def get_products(self) -> list[Product]:
        """
        Абстрактный метод доступа к данным о товарах.
        Требует конкретной реализации в классах наследниках.
        """


# pylint: disable=too-few-public-methods
class CsvProductProvider(ProductProvider):
    """
    Класс реализующий доступ к данным в CSV файлах
    """

    def __init__(self, logger: logging.Logger = None):
        super().__init__(logger=logger)

    def get_products(self) -> list[Product]:
        try:
            with open("products.csv", encoding='utf-8') as file:
                products = list(csv.DictReader(file, delimiter=";"))
            return [
                Product(name=product["name"],
                        price=float(product["price"].replace(",", ".")),
                        description=product["description"],
                        quantity=int(product["quantity"]))
                for product in products
            ]
        except FileNotFoundError:
            self.logger.error("Файл не найден")
            return []
        except PermissionError:
            self.logger.error("Ошибка прав доступа к файлу")
            return []
        except csv.Error:
            print("Ошибка CSV")
            return []


# pylint: disable=too-few-public-methods
class DatabaseProductProvider(ProductProvider):
    """
    Класс реализующий доступ к данным в БД
    """

    def __init__(self, logger: logging.Logger = None):
        warnings.warn("Этот класс еще не реализован", UserWarning)
        super().__init__(logger=logger)

    def get_products(self) -> list[Product]:
        raise NotImplementedError


# pylint: disable=too-few-public-methods
class ApiProductProvider(ProductProvider):
    """
    Класс реализующий доступ к данным через API
    """

    def __init__(self, logger: logging.Logger = None):
        warnings.warn("Этот класс еще не реализован", UserWarning)
        super().__init__(logger=logger)

    def get_products(self) -> list[Product]:
        raise NotImplementedError
