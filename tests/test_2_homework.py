# coding: utf-8
from selene import be, have


def test_homework_2(browser_density):
    browser_density.open('https://google.com')
    random_string = "uyfihfhgfxcjkjhkljljkhjfgfchghvkjggfhhglkgfgdjvhjklllkl,lkjhjghfgcjh"
    browser_density.element('[name="q"]').should(be.blank).type(random_string).press_enter()
    browser_density.element('//*[@id="botstuff"]/div/div[2]/div/p[1]').should(
        have.text(f'По запросу {random_string} ничего не найдено.'))
