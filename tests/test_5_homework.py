# coding: utf-8
import os
from selene import be, have, command
from pages.page_automation_practice_form import PageAutomationPracticeForm


def test_main_positive(browser_den):
    browser_den.open("https://demoqa.com/automation-practice-form")

    browser_den.element('#firstName').perform(command.js.scroll_into_view).should(be.blank).type('Klim')
    browser_den.element('#lastName').perform(command.js.scroll_into_view).should(be.blank).type('Molokov')
    browser_den.element('#userEmail').perform(command.js.scroll_into_view).type('super@test.com')
    browser_den.all('[name=gender]').element_by(have.value('Male')).element('..').perform(command.js.scroll_into_view).click()
    browser_den.element('#userNumber').perform(command.js.scroll_into_view).type('8123123123')

    browser_den.element('#dateOfBirthInput').perform(command.js.scroll_into_view).click()
    browser_den.element('.react-datepicker__month-select').perform(command.js.scroll_into_view).send_keys("March")
    browser_den.element('#dateOfBirthInput').perform(command.js.scroll_into_view).click()
    browser_den.element('.react-datepicker__year-select').send_keys("1989")
    browser_den.element('#dateOfBirthInput').perform(command.js.scroll_into_view).click()
    browser_den.element(f'.react-datepicker__day--005').click()
    browser_den.element('#subjectsInput').perform(command.js.scroll_into_view).send_keys("some objects")
    browser_den.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Sports')).perform(command.js.scroll_into_view).click()
    browser_den.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Reading')).perform(command.js.scroll_into_view).click()
    browser_den.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Music')).perform(command.js.scroll_into_view).click()
    browser_den.element('#uploadPicture').perform(command.js.scroll_into_view).send_keys(os.path.abspath('tests/test_data/1.bmp'))
    browser_den.element('#currentAddress').perform(command.js.scroll_into_view).type("some address 186")
    browser_den.element('#state').click().perform(command.js.scroll_into_view)
    browser_den.all('[id^=react-select][id*=option]').element_by(have.exact_text('Uttar Pradesh')).click()
    browser_den.element('#city').click().perform(command.js.scroll_into_view)
    browser_den.all('[id^=react-select][id*=option]').element_by(have.exact_text('Agra')).click()
    browser_den.element('#currentAddress').perform(command.js.scroll_into_view).submit()

    browser_den.all('.table-responsive .table td:nth-child(2)').should(have.exact_texts(
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

