from datetime import datetime

from selene import have, command
from selene.core.entity import Element, Collection, Browser
from selenium.webdriver import Keys


class PageAutomationPracticeForm:
    """
    https://demoqa.com/automation-practice-form
    """

    def __init__(self, browser: Browser):
        self.browser = browser
        self.browser.open("https://demoqa.com/automation-practice-form")

    @property
    def first_name(self) -> Element:
        """
        edit text
        """
        return self.browser.element('#firstName').perform(command.js.scroll_into_view)

    @property
    def last_name(self) -> Element:
        """
        edit text
        """
        return self.browser.element('#lastName').perform(command.js.scroll_into_view)

    @property
    def email(self) -> Element:
        """
        edit text
        """
        return self.browser.element('#userEmail').perform(command.js.scroll_into_view)

    @property
    def gender_male(self) -> Element:
        """
        radio button
        """
        return self.browser.all('[name=gender]').element_by(have.value('Male')).element('..').perform(command.js.scroll_into_view)

    @property
    def gender_female(self) -> Element:
        """
        radio button
        """
        return self.browser.all('[name=gender]').element_by(have.value('Female')).element('..').perform(command.js.scroll_into_view)

    @property
    def gender_other(self) -> Element:
        """
        radio button
        """
        return self.browser.all('[name=gender]').element_by(have.value('Other')).element('..').perform(command.js.scroll_into_view)

    @property
    def phone(self) -> Element:
        """
        edit text
        """
        return self.browser.element('#userNumber').perform(command.js.scroll_into_view)

    @property
    def date_of_birth(self) -> Element:
        """
        edit text
        """
        return self.browser.element('#dateOfBirthInput').perform(command.js.scroll_into_view)

    @property
    def date_of_birth_modal_month(self) -> Element:
        """
        modal
        """
        self.date_of_birth.click()
        return self.browser.element('.react-datepicker__month-select').perform(command.js.scroll_into_view)

    @property
    def date_of_birth_modal_year(self) -> Element:
        """
        modal
        """
        self.date_of_birth.click().perform(command.js.scroll_into_view)
        return self.browser.element('.react-datepicker__year-select')

    @property
    def date_of_birth_modal_day(self):
        def inner_function(day: str) -> Element:
            """
            modal
            """
            self.date_of_birth.click().perform(command.js.scroll_into_view)
            return self.browser.element(f'.react-datepicker__day--0{day}')
        return inner_function

    @property
    def subjects(self) -> Element:
        """
        edit text
        """
        return self.browser.element('#subjectsInput').perform(command.js.scroll_into_view)

    @property
    def hobbie_sports(self) -> Element:
        """
        radio button
        """
        return self.browser.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Sports')).perform(command.js.scroll_into_view)

    @property
    def hobbie_reading(self) -> Element:
        """
        radio button
        """
        return self.browser.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Reading')).perform(command.js.scroll_into_view)

    @property
    def hobbie_music(self) -> Element:
        """
        radio button
        """
        return self.browser.all('#hobbiesWrapper .custom-control-label').element_by(have.exact_text('Music')).perform(command.js.scroll_into_view)

    @property
    def upload_file(self) -> Element:
        """
        button
        """
        return self.browser.element('#uploadPicture').perform(command.js.scroll_into_view)

    @property
    def current_address(self) -> Element:
        """
        edit text
        """
        return self.browser.element('#currentAddress').perform(command.js.scroll_into_view)

    @property
    def state(self):
        def inner_function(state: str) -> Element:
            """
            drop down menu
            """
            self.browser.element('#state').click().perform(command.js.scroll_into_view)
            return self.browser.all('[id^=react-select][id*=option]').element_by(have.exact_text(state))
        return inner_function

    @property
    def city(self):
        def inner_function(city: str) -> Element:
            """
            drop down menu
            """
            self.browser.element('#city').click().perform(command.js.scroll_into_view)
            return self.browser.all('[id^=react-select][id*=option]').element_by(have.exact_text(city))
        return inner_function

    @property
    def submit(self):
        return self.browser.element('#submit')

    @property
    def final_table(self):
        return self.browser.all('.table-responsive .table td:nth-child(2)')
