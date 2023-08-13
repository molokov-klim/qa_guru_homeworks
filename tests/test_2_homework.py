# coding: utf-8
from selene import be, have
from selene import browser


def test_homework_2():
    browser.open('https://google.com')
    random_string = "uyfihfhgfxcjkjhkljljkhjfgfchghvkjggfhhglkgfgdjvhjklllkl,lkjhjghfgcjh"
    browser.element('[name="q"]').should(be.blank).type(random_string).press_enter()
    browser.element('//*[@id="botstuff"]/div/div[2]/div/p[1]').should(
        have.text(f'По запросу {random_string} ничего не найдено.'))