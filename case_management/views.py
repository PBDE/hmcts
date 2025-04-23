from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from datetime import datetime

from . forms import LoginForm, CreateTaskForm
from . enums import PatternNames
from . models import Task, TaskHistory, TaskNote
from . text import USER_GREETING_TEXT, LOGIN_ERROR_MESSAGE

LOGIN_TEMPLATE = "case_management/login.html"
CASE_OVERVIEW_TEMPLATE = "case_management/case_overview.html"
CREATE_TASK_TEMPLATE = "case_management/create_task.html"

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(PatternNames.CASES_OVERVIEW.value)
        )
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse(PatternNames.CASES_OVERVIEW.value)
                )
        return render(request, 
                      LOGIN_TEMPLATE, 
                      {"form": login_form, 
                       "message": LOGIN_ERROR_MESSAGE}
        )
    return render(request, LOGIN_TEMPLATE, {
        "form": LoginForm()
    })

def case_overview_view(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(PatternNames.LOGIN.value))
    
    tasks = Task.objects.all()

    return render(
        request, 
        CASE_OVERVIEW_TEMPLATE, {
            'greeting_message': USER_GREETING_TEXT, 
            "tasks": tasks
        }
    )

def create_task_view(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(PatternNames.LOGIN.value))

    if request.method == "POST":
        new_task_form = CreateTaskForm(request.POST)

        if new_task_form.is_valid():
            title = new_task_form.cleaned_data["title"]
            due_date = new_task_form.cleaned_data["due_date"]
            description = new_task_form.cleaned_data["description"]

            new_task = Task(title=title, due_date=due_date)
            new_task.save()

            new_task_history = TaskHistory(
                status="U",
                task=new_task, 
                created_by=request.user
            )
            new_task_history.save()

            if description:
                new_task_note = TaskNote(
                    description=description, 
                    task=new_task, 
                    created_by=request.user
                )
                new_task_note.save()
        else:
            return render(request, CREATE_TASK_TEMPLATE, {"form": new_task_form })

    return render(request, CREATE_TASK_TEMPLATE, {"form": CreateTaskForm()})
