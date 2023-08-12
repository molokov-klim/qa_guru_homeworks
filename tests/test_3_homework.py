# coding: utf-8
import math


def test_greeting():
    """
    Напишите программу, которая выводит на экран приветствие.
    """
    name = "Анна"
    age = 25
    output = f"Привет, {name}! Тебе {age} лет."
    # Проверяем результат
    assert output == "Привет, Анна! Тебе 25 лет."


def test_rectangle():
    """
    Напишите программу, которая берет длину и ширину прямоугольника
    и считает его периметр и площадь.
    """
    a = 10
    b = 20

    perimeter = 2 * (a + b)

    assert perimeter == 60

    area = a * b
    assert area == 200


def test_circle():
    """
    Напишите программу, которая берет радиус круга и выводит на экран его длину и площадь.
    Используйте константу PI
    """

    r = 23
    area = math.pi * r ** 2
    assert area == 1661.9025137490005

    length = 2 * (math.pi * r)
    assert length == 144.51326206513048


def test_random_list():
    """
    Создайте список из 10 случайных чисел от 1 до 100 и отсортируйте его по возрастанию.
    """

    digit_list = []
    for i in range(11):
        digit_list.append(i * 10)
    digit_list.pop(0)
    digit_list.sort()   # действие лишнее, но по заданию необходимо отсортировать

    assert len(digit_list) == 10
    assert digit_list[0] < digit_list[-1]


def test_unique_elements():
    """
    Удалите из списка все повторяющиеся элементы
    """
    digit_list = [1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 8, 9, 10, 10]

    digit_list = list(set(digit_list))

    assert isinstance(digit_list, list)
    assert len(digit_list) == 10
    assert digit_list == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_dicts():
    """
    Создайте словарь из двух списков.
    Используйте первый список как ключи, а второй - как значения.
    Выведите на экран все значения словаря.
    Подсказка: используй встроенную функцию zip.
    """
    first = ["a", "b", "c", "d", "e"]
    second = [1, 2, 3, 4, 5]
    d = dict(zip(first, second))

    assert isinstance(d, dict)
    assert len(d) == 5
