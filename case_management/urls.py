from django.urls import path
from . import views

app_name = "case_management"
urlpatterns = [
    path("", views.login_view, name="login"),
    path("cases", views.case_overview_view, name="cases_overview")
]