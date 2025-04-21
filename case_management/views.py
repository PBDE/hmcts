from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

from . forms import LoginForm

LOGIN_TEMPLATE = "case_management/login.html"
LOGIN_REDIRECT_PATTERN_NAME = "case_management:case_overview"
LOGIN_ERROR_MESSAGE = "Details did not match those of an existing user"

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(LOGIN_REDIRECT_PATTERN_NAME, 
                                            kwargs={"user": request.user.username})
        )
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse(LOGIN_REDIRECT_PATTERN_NAME, 
                                                    kwargs={"user": username})
                )
        return render(request, 
                      LOGIN_TEMPLATE, 
                      {"form": login_form, 
                       "message": LOGIN_ERROR_MESSAGE}
        )
    return render(request, LOGIN_TEMPLATE, {
        "form": LoginForm()
    })
