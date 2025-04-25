from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from . forms import LoginForm, CreateTaskForm, UpdateTaskStatusForm, AddNoteForm
from . enums import PatternNames
from . models import Task, TaskHistory, TaskNote
from . text import USER_GREETING_TEXT, LOGIN_ERROR_MESSAGE

LOGIN_TEMPLATE = "case_management/login.html"
CASE_OVERVIEW_TEMPLATE = "case_management/case_overview.html"
CREATE_TASK_TEMPLATE = "case_management/create_task.html"
TASK_TEMPLATE = "case_management/task.html"
TASK_NOT_FOUND_TEMPLATE = "case_management/task_not_found.html"

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
        CASE_OVERVIEW_TEMPLATE, 
        {
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

            return HttpResponseRedirect(reverse(PatternNames.CASES_OVERVIEW.value))

        else:
            return render(request, CREATE_TASK_TEMPLATE, {"form": new_task_form })

    return render(request, CREATE_TASK_TEMPLATE, {"form": CreateTaskForm()})

def task_view(request, slug):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(PatternNames.LOGIN.value))

    task = Task.objects.filter(slug=slug).first() # check for empty task

    if not task:
        return render(request, TASK_NOT_FOUND_TEMPLATE)


    if "status_form" in request.POST:
        update_status_form = UpdateTaskStatusForm(request.POST)
        if update_status_form.is_valid():
            status_update = update_status_form.cleaned_data["status"]
            new_status = TaskHistory(
                status=status_update,
                task=task,
                created_by=request.user
                )
            new_status.save()

    if "note_form" in request.POST:

        add_note_form = AddNoteForm(request.POST)
        if add_note_form.is_valid():
            note_text = add_note_form.cleaned_data["note"]
            new_note = TaskNote(
                description=note_text,
                task=task,
                created_by=request.user
            )
            new_note.save()
    
    if "delete_form" in request.POST:
        print("delete")
        task.delete()
        return HttpResponseRedirect(reverse(PatternNames.CASES_OVERVIEW.value))

    task_histories = TaskHistory.objects.filter(task=task)
    task_notes = TaskNote.objects.filter(task=task)
    
    return render(
        request,
        TASK_TEMPLATE, 
        {
            "task": task,
            "task_history": task_histories,
            "task_notes": task_notes,
            "status_form": UpdateTaskStatusForm(),
            "note_form": AddNoteForm()
        }
    )

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(PatternNames.LOGIN.value))
