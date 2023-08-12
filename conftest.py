# coding: utf-8
import logging

import pytest
from selene import browser
from selenium import webdriver
from selenium.common import WebDriverException


@pytest.fixture(scope="session")
def browser_density(request):
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    def browser_finalizer(browser):
        """
        Функция финализации после выполнения теста.

        Args:
            browser: Объект WebDriver для работы с браузером.
        """
        try:
            browser.quit()  # Закрытие браузера
        except WebDriverException as e:
            logging.error("Browser is already closed or crashed")

    yield browser
    request.addfinalizer(lambda: browser_finalizer(browser))


@pytest.fixture(scope="session")
def browser_headless(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # additional options:
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    options.add_argument('--enable-automation')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    browser.config.driver_options = options

    def browser_finalizer(browser):
        """
        Функция финализации после выполнения теста.

        Args:
            browser: Объект WebDriver для работы с браузером.
        """
        try:
            browser.quit()  # Закрытие браузера
        except WebDriverException as e:
            logging.error("Browser is already closed or crashed")

    yield browser
    request.addfinalizer(lambda: browser_finalizer(browser))
