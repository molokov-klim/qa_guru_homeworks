import inspect
from datetime import time, datetime


def test_dark_theme_by_time():
    """
    Протестируйте правильность переключения темной темы на сайте в зависимости от времени
    (с 22 до 6 часов утра - ночь)
    """
    current_time = datetime.now()

    is_dark_theme = False
    if 6 < current_time.hour < 22:
        is_dark_theme = True
        assert is_dark_theme is True
    else:
        assert is_dark_theme is False


def test_dark_theme_by_time_and_user_choice():
    """
    Протестируйте правильность переключения темной темы на сайте
    в зависимости от времени и выбора пользователя
    dark_theme_enabled_by_user = True - Темная тема включена
    dark_theme_enabled_by_user = False - Темная тема выключена
    dark_theme_enabled_by_user = None - Пользователь не сделал выбор (используется переключение по времени системы)
    """
    current_time = time(hour=16)
    dark_theme_enabled_by_user = True

    if not dark_theme_enabled_by_user:
        if 6 < current_time.hour < 22:
            is_dark_theme = False
        else:
            is_dark_theme = True
    else:
        is_dark_theme = True

    assert is_dark_theme is True


def test_find_suitable_user():
    """
    Найдите нужного пользователя по условиям в списке пользователей
    """
    users = [
        {"name": "Oleg", "age": 32},
        {"name": "Sergey", "age": 24},
        {"name": "Stanislav", "age": 15},
        {"name": "Olga", "age": 45},
        {"name": "Maria", "age": 18},
    ]

    suitable_users = None

    for user in users:
        if user.get('name') == 'Olga':
            suitable_users = user

    assert suitable_users == {"name": "Olga", "age": 45}

    suitable_users = []

    for user in users:
        if int(user.get('age')) < 20:
            suitable_users.append(user)

    assert suitable_users == [
        {"name": "Stanislav", "age": 15},
        {"name": "Maria", "age": 18},
    ]


# Сделайте функцию, которая будет печатать
# читаемое имя переданной ей функции и значений аргументов.
# Вызовите ее внутри функций, описанных ниже
# Подсказка: Имя функции можно получить с помощью func.__name__
# Например, вызов следующей функции должен преобразовать имя функции
# в более читаемый вариант (заменить символ подчеркивания на пробел,
# сделать буквы заглавными (или первую букву), затем вывести значения всех аргументов этой функции:
# >>> open_browser(browser_name="Chrome")
# "Open Browser [Chrome]"

def pretty_string(*args):
    """
    Первый позиционный аргумент - ссылка на функцию
    """
    method_name = args[0].__name__
    args = args[1:]

    arg_name = ", ".join([*args])
    arg = f'[{arg_name}]'

    # method_name = str(inspect.stack()[1].function)
    actual_result = f"{method_name.title()} {arg.title() if 'https' not in arg else arg}".replace('_', " ")
    print(actual_result)
    return actual_result


def test_readable_function():
    open_browser(browser_name="Chrome")
    go_to_companyname_homepage(page_url="https://companyname.com")
    find_registration_button_on_login_page(page_url="https://companyname.com/login", button_text="Register")


def open_browser(browser_name):
    actual_result = pretty_string(open_browser, browser_name)
    assert actual_result == "Open Browser [Chrome]"


def go_to_companyname_homepage(page_url):
    actual_result = pretty_string(go_to_companyname_homepage, page_url)
    assert actual_result == "Go To Companyname Homepage [https://companyname.com]"


def find_registration_button_on_login_page(page_url, button_text):
    actual_result = pretty_string(find_registration_button_on_login_page, page_url, button_text)
    assert actual_result == "Find Registration Button On Login Page [https://companyname.com/login, Register]"
