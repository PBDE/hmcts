from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from unittest import skip
from time import time, sleep

from case_management.tests.test_utils import create_temporary_user, create_new_task_data

class FunctionalTestCase(StaticLiveServerTestCase):

    SELECTOR_USERNAME_INPUT = "input#id_username"
    SELECTOR_PASSWORD_INPUT = "input#id_password"
    SELECTOR_LOGIN_BTN = "input.submit-btn"
    SELECTOR_CASE_OVERVIEW_HEADER_TEXT = ".cases-overview-txt"
    SELECTOR_LOGIN_FORM = "form.login-form"
    SELECTOR_CREATE_TASK_LINK = "a.create-task-link"
    SELECTOR_CREATE_TASK_FORM = "form.create-task-form"
    SELECTOR_TASK_TITLE_INPUT = "input#id_title"
    SELECTOR_TASK_DUE_DATE_INPUT = "input#id_due_date"
    SELECTOR_TASK_CREATE_BTN = "input.submit-btn"
    SELECTOR_SELECT_TASK_LINK = "a.task-link"
    SELECTOR_TASK_HEADER_TEXT = ".task-header-text"

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
            self.fail(f"Selector not found: {e}")

        # the registered user is redirected to their user page
        try:
            self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_CASE_OVERVIEW_HEADER_TEXT))
        except NoSuchElementException:
            self.fail(f"Header with {self.SELECTOR_CASE_OVERVIEW_HEADER_TEXT} selector not found")

        return username, email, password

    def create_new_task(self):
        new_task_data = create_new_task_data()

        # enter create task details
        try:
            self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_TASK_TITLE_INPUT).send_keys(new_task_data["title"])
            self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_TASK_DUE_DATE_INPUT).send_keys(str(new_task_data["due_date"]))
        except NoSuchElementException as e:
            self.fail(f"Selector not found: {e}")

        # submit create task form
        try:
            self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_TASK_CREATE_BTN).click()
        except NoSuchElementException as e:
            self.fail(f"Button with {self.SELECTOR_TASK_CREATE_BTN} selector not found")

class LandingPageTestCase(FunctionalTestCase):

    def test_user_can_log_in(self):

        from case_management.text import USER_GREETING_TEXT

        self.browser.get(self.live_server_url)

        # the user sees the log in form
        try:
            self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_LOGIN_FORM)
        except NoSuchElementException:
            self.fail(f"Login form with {self.SELECTOR_LOGIN_FORM} selector not found")

        # the user enters their login details
        username, _, _ = self.login_temporary_user()

        # the user sees the greeting
        try:
            greeting_text = self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_CASE_OVERVIEW_HEADER_TEXT).text
            self.assertIn(USER_GREETING_TEXT + username, greeting_text)
        except NoSuchElementException:
            self.fail(f"Header text with {self.SELECTOR_CASE_OVERVIEW_HEADER_TEXT} selector not found")

    @skip
    def test_incorrect_login_details(self):
        self.fail("Not implemented")

class CaseOverviewTestCase(FunctionalTestCase):

    def test_user_can_create_task(self):

        self.browser.get(self.live_server_url)
        self.login_temporary_user()

        # find the create task button
        try:
            create_task_link = self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_CREATE_TASK_LINK)
        except NoSuchElementException:
            self.fail(f"Button with {self.SELECTOR_CREATE_TASK_LINK} selector not found")

        # click create task button
        create_task_link.click()

        # wait for create task form to load
        try:
            self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_CREATE_TASK_FORM))
        except NoSuchElementException:
            self.fail(f"Form with {self.SELECTOR_CREATE_TASK_FORM} selector not found")

        self.create_new_task()

        # check that new task added to the list
        self.fail("IMPLEMENT: Check that the task is added to the list")
        
    def test_user_can_select_task(self):

        self.browser.get(self.live_server_url)
        self.login_temporary_user()
        self.create_new_task()

        try:
            task_link = self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_SELECT_TASK_LINK)
            task_link.click()
        except NoSuchElementException:
            self.fail(f"Link with {self.SELECTOR_SELECT_TASK_LINK} selector not found")

        try:
            self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, self.SELECTOR_TASK_HEADER_TEXT))
        except:
            self.fail(f"Header with {self.SELECTOR_TASK_HEADER_TEXT} selector not found")    
        
class TaskPageTestCase(FunctionalTestCase):

    @skip
    def test_user_can_delete_task(self):

        # login
        # go to the task creation page
        # create task
        # select task
        # click delete task button
        # check task no longer exists

        self.fail("Not implemented")

    @skip
    def test_user_can_update_task_status(self):

        # login
        # go to the task creation page
        # create task
        # select task
        # click the update task button
        # enter the new status
        # check the status

        self.fail("Not implemented")

    @skip
    def test_user_can_add_notes(self):
        self.fail("Not implemented")
    