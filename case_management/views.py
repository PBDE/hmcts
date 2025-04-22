from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from . forms import LoginForm
from . enums import PatternNames
from . text import USER_GREETING_TEXT, LOGIN_ERROR_MESSAGE

LOGIN_TEMPLATE = "case_management/login.html"
CASE_OVERVIEW_TEMPLATE = "case_management/case_overview.html"

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
    return render(request, CASE_OVERVIEW_TEMPLATE, {'greeting_message': USER_GREETING_TEXT})
