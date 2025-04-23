from unittest import skip
from django.test import TestCase, Client
from django.urls import reverse

from case_management.forms import LoginForm, CreateTaskForm
from case_management.tests.test_utils import create_user_data, create_temporary_user, create_new_task_data
from case_management.enums import PatternNames
from case_management.views import LOGIN_TEMPLATE, CREATE_TASK_TEMPLATE
from case_management.text import LOGIN_ERROR_MESSAGE
from case_management.models import Task, TaskNote, TaskHistory

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

class CaseOverviewViewTest(TestCase):
    
    def login_temporary_user(self):
        username, _, password = create_temporary_user()
        self.client.post(
            reverse(PatternNames.LOGIN.value), 
            data={
                "username": username, 
                "password": password}, 
            follow=True
        )

    def test_overview_template_returned(self):

        self.login_temporary_user()
        response = self.client.get(reverse(PatternNames.CREATE_TASK.value))
        self.assertTemplateUsed(response, CREATE_TASK_TEMPLATE)

    def test_create_task_form_returned(self):

        self.login_temporary_user()
        response = self.client.get(reverse(PatternNames.CREATE_TASK.value))
        self.assertIsInstance(response.context["form"], CreateTaskForm)

    def test_new_task_created(self):

        self.login_temporary_user()
        new_task_data = create_new_task_data()
        self.client.post(reverse(PatternNames.CREATE_TASK.value), data=new_task_data)

        # check the new task has been created
        self.assertEqual(Task.objects.count(), 1)
        new_task = Task.objects.first()
        self.assertEqual(new_task.title, new_task_data["title"])

        # check that a new task history has been created
        self.assertEqual(TaskHistory.objects.count(), 1)
        new_task_history = TaskHistory.objects.first()
        self.assertEqual(new_task_history.task, new_task)

        # check that the a new task note has been created
        self.assertEqual(TaskNote.objects.count(), 1)
        new_task_note = TaskHistory.objects.first()
        self.assertEqual(new_task_note.task, new_task)

    @skip
    def test_user_redirected_after_task_created(self):
        ...

    @skip
    def test_invalid_task_response_contains_task_form(self):
        ...

    
