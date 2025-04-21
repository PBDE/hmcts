from django.urls import path
from . import views

app_name = "case_management"
urlpatterns = [
    path("", views.login, name="login"),
    path("cases", views.case_overview, name="case_overview")
]