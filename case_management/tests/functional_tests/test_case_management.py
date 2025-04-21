from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from unittest import skip

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()


class LandingPageTests(FunctionalTest):

    def test_user_can_log_in(self):

        FORM_SELECTOR = "form.login-form"

        self.browser.get(self.live_server_url)

        # the user sees the log in form
        try:
            self.browser.find_element(By.CSS_SELECTOR, FORM_SELECTOR)
        except NoSuchElementException:
            self.fail(f"Login form with selector {FORM_SELECTOR} not found")

        # the user enters their login details


    @skip
    def test_logged_in_user_redirected(self):
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
    