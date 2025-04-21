from django.shortcuts import render

LOGIN_TEMPLATE = "case_management/login.html"

def login(request):
    return render(request, LOGIN_TEMPLATE)
