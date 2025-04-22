from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from case_management.forms import LoginForm
from case_management.tests.test_utils import create_user_data, create_temporary_user
from case_management.enums import PatternNames

from case_management.views import LOGIN_TEMPLATE
from case_management.text import LOGIN_ERROR_MESSAGE

class LoginViewTest(TestCase):

    def test_authenticated_user_redirected(self):
        username, _, password = create_temporary_user()
        client = Client()
        client.login(username=username, password=password)
        response = client.get(reverse(PatternNames.LOGIN.value))
        self.assertRedirects(response, reverse(PatternNames.CASES_OVERVIEW.value))

    def test_login_template_returned(self):
        response = self.client.get(reverse(PatternNames.LOGIN.value))
        self.assertTemplateUsed(response, LOGIN_TEMPLATE)

    def test_login_form_returned(self):
        response = self.client.get(reverse(PatternNames.LOGIN.value))
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_user_is_logged_in(self):
        username, _, password = create_temporary_user()
        response = self.client.post(
            reverse(PatternNames.LOGIN.value), 
            data={
                "username": username, 
                "password": password}, 
            follow=True
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_user_is_rediredted_after_login(self):
        username, _, password = create_temporary_user()
        response = self.client.post(reverse(PatternNames.LOGIN.value), 
                                    data={"username": username, 
                                          "password": password})
        self.assertRedirects(response, reverse(PatternNames.CASES_OVERVIEW.value))

    def test_invalid_login_returns_login_template(self):
        create_temporary_user()
        incorrect_user_data = create_user_data()
        response = self.client.post(reverse(PatternNames.LOGIN.value), 
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password"]})
        self.assertTemplateUsed(response, LOGIN_TEMPLATE)

    def test_invalid_login_response_contains_login_form(self):
        create_temporary_user()
        incorrect_user_data = create_user_data()
        response = self.client.post(reverse(PatternNames.LOGIN.value),
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password"]})
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_invalid_login_contains_error_message(self):
        create_temporary_user()
        incorrect_user_data = create_user_data()
        response = self.client.post(reverse(PatternNames.LOGIN.value), 
                                    data={"username": incorrect_user_data["username"],
                                          "password": incorrect_user_data["password"]})
        self.assertContains(response, LOGIN_ERROR_MESSAGE)
