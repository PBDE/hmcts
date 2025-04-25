from django import forms
from . models import TITLE_MAX_LENGTH, TaskHistory

class LoginForm(forms.Form):

    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

class CreateTaskForm(forms.Form):
    
    title = forms.CharField(label="Task Title", max_length=TITLE_MAX_LENGTH)
    due_date = forms.DateField(label="Due Date")
    description = forms.CharField(label="Description", required=False)

class UpdateTaskStatusForm(forms.Form):
    status = forms.ChoiceField(choices=TaskHistory.STATUS_OPTIONS)

class AddNoteForm(forms.Form):
    note = forms.CharField()
    