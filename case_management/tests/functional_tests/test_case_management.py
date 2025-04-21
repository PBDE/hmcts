from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from unittest import skip
from selenium.common.exceptions import WebDriverException
from time import time, sleep

from case_management.tests.test_utils import create_temporary_user

class FunctionalTest(StaticLiveServerTestCase):

    SELECTOR_USERNAME_INPUT = "input#id_username"
    SELECTOR_PASSWORD_INPUT = "input#id_password"
    SELECTOR_LOGIN_BTN = "input.submit-btn"
    SELECTOR_CASE_OVERVIEW_HEADER_TEXT = ".cases-overview-txt"
    SELECTOR_LOGIN_FORM = "form.login-form"

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for(self, fn):

        MAX_WAIT = 10
        start_time = time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as errors:
                if time() - start_time > MAX_WAIT:
                    raise errors
                sleep(0.5)

    def login_temporary_user(self):

        username, email, password = create_temporary_user()

        # the user goes to the login page
        self.browser.get(self.live_server_url)

        # the user enters their username and password and clicks login

        try:
            self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_USERNAME_INPUT).send_keys(username)
            self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_PASSWORD_INPUT).send_keys(password)
            self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_LOGIN_BTN).click()
        except NoSuchElementException as e:
            self.fail("Selector not found: " + e)

        # the registered user is redirected to their user page
        try:
            self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_CASE_OVERVIEW_HEADER_TEXT))
        except NoSuchElementException:
            self.fail(f"Header with selector {self.SELECTOR_CASE_OVERVIEW_HEADER_TEXT} not found")

        return username, email, password


class LandingPageTests(FunctionalTest):

    def test_user_can_log_in(self):

        from case_management.text import USER_GREETING_TEXT

        self.browser.get(self.live_server_url)

        # the user sees the log in form
        try:
            self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_LOGIN_FORM)
        except NoSuchElementException:
            self.fail(f"Login form with selector {self.SELECTOR_LOGIN_FORM} not found")

        # the user enters their login details
        username, _, _ = self.login_temporary_user()

        # the user sees the greeting
        try:
            greeting_text = self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_CASE_OVERVIEW_HEADER_TEXT).text
            self.assertIn(USER_GREETING_TEXT + username, greeting_text)
        except NoSuchElementException:
            self.fail(f"Header text with selector {self.SELECTOR_CASE_OVERVIEW_HEADER_TEXT} not found")

    @skip
    def test_incorrect_login_details(self):
        self.fail("Not implemented")

class UserPageTests(FunctionalTest):

    @skip
    def test_user_can_create_task(self):
        self.fail("Not implemented")

    @skip
    def test_user_can_select_task(self):
        self.fail("Not implemented")
        
class TaskPageTests(FunctionalTest):

    @skip
    def test_user_can_update_task_status(self):
        self.fail("Not implemented")

    @skip
    def test_user_can_add_notes(self):
        self.fail("Not implemented")

    @skip
    def test_user_can_delete_task(self):
        self.fail("Not implemented")
    