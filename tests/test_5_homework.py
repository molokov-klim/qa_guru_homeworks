# coding: utf-8
import os
from selene import be, have, command
from selene import browser


def test_main_positive():
    browser.open("https://demoqa.com/automation-practice-form")

    browser.element('#firstName').perform(command.js.scroll_into_view).should(be.blank).type('Klim')
    browser.element('#lastName').should(be.blank).type('Molokov')
    browser.element('#userEmail').type('super@test.com')
    browser.all('[name=gender]').element_by(have.value('Male')).element('..').click()
    browser.element('#userNumber').type('8123123123')

    browser.element('#dateOfBirthInput').perform(command.js.scroll_into_view).click()
    browser.element('.react-datepicker__month-select').send_keys("March")
    browser.element('#dateOfBirthInput').click()
    browser.element('.react-datepicker__year-select').send_keys("1989")
    browser.element('#dateOfBirthInput').click()
    browser.element(f'.react-datepicker__day--005').click()
    browser.element('#subjectsInput').send_keys("some objects")
    browser.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Sports')).click()
    browser.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Reading')).click()
    browser.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Music')).click()
    browser.element('#uploadPicture').perform(command.js.scroll_into_view).send_keys(os.path.abspath('tests/test_data/1.bmp'))
    browser.element('#currentAddress').type("some address 186")
    browser.element('#state').click()
    browser.all('[id^=react-select][id*=option]').element_by(have.exact_text('Uttar Pradesh')).click()
    browser.element('#city').click().perform(command.js.scroll_into_view)
    browser.all('[id^=react-select][id*=option]').element_by(have.exact_text('Agra')).click()
    browser.element('#currentAddress').submit()

    browser.all('.table-responsive .table td:nth-child(2)').should(have.exact_texts(
        'Klim Molokov',
        'super@test.com',
        'Male',
        '8123123123',
        '05 March,1989',
        '',
        'Sports, Reading, Music',
        '1.bmp',
        'some address 186',
        'Uttar Pradesh Agra'
    ))

