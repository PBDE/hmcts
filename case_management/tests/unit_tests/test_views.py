from django.test import TestCase
from django.urls import reverse

from case_management.views import LOGIN_TEMPLATE

class LoginViewTest(TestCase):

    def test_login_template_returned(self):
        response = self.client.get(reverse("case_management:login"))
        self.assertTemplateUsed(response, LOGIN_TEMPLATE)
