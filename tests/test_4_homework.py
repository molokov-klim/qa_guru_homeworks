# coding: utf-8
import os
from selene import be, have
from pages.page_automation_practice_form import PageAutomationPracticeForm


def test_main_positive(browser_density):
    page = PageAutomationPracticeForm(browser_density)

    page.first_name.should(be.blank).type('Klim')
    page.last_name.should(be.blank).type('Molokov')
    page.email.type('super@test.com')
    page.gender_male.click()
    page.phone.type('8123123123')
    page.date_of_birth_modal_month.send_keys("March")
    page.date_of_birth_modal_year.send_keys("1989")
    page.date_of_birth_modal_day(day="05").click()
    page.subjects.send_keys("some objects")
    page.hobbie_reading.click()
    page.hobbie_sports.click()
    page.hobbie_music.click()
    page.upload_file.send_keys(os.path.abspath('tests/test_data/1.bmp'))
    page.current_address.type("some address 186")
    page.state('Uttar Pradesh').click()
    page.city('Agra').click()
    page.current_address.submit()

    page.final_table.should(have.exact_texts(
        'Klim Molokov',
        'super@test.com',
        'Male',
        '8123123123',
        '05 March,1989',
        '',
        'Reading, Sports, Music',
        '1.bmp',
        'some address 186',
        'Uttar Pradesh Agra'
    ))
