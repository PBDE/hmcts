from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from unittest import skip


class LandingPageTests(StaticLiveServerTestCase):

    @skip
    def test_user_can_log_in(self):

        self.browser.get(self.live_server_url)
        self.fail("Not implemented")

    @skip
    def test_logged_in_user_redirected(self):
        self.fail("Not implemented")

class UserPageTests(StaticLiveServerTestCase):

    @skip
    def test_user_can_create_task(self):
        self.fail("Not implemented")

    @skip
    def test_user_can_select_task(self):
        self.fail("Not implemented")
        
class TaskPageTests(StaticLiveServerTestCase):

    @skip
    def test_user_can_update_task_status(self):
        self.fail("Not implemented")

    @skip
    def test_user_can_add_notes(self):
        self.fail("Not implemented")

    @skip
    def test_user_can_delete_task(self):
        self.fail("Not implemented")
    