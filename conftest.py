# coding: utf-8
import pytest
from selene.support.shared import browser
from selene import be, have


@pytest.fixture(scope="session")
def browser_configured():
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield browser
    browser.close()




