from string import ascii_letters, digits, punctuation
from random import randint
from django.contrib.auth import get_user_model
from datetime import date

from case_management.enums import UserDetails
from case_management.models import Task, TaskHistory, TaskNote

def random_user_details(input_field_type):

    match input_field_type:
        case UserDetails.USERNAME:
            characters = ascii_letters + digits + "@.+-_"
        case UserDetails.PASSWORD:
            characters = ascii_letters + digits + punctuation
        case UserDetails.EMAIL:
            characters = ascii_letters + digits + "._"

    user_detail = ""
    for _ in range(randint(10, 20)):
        user_detail += characters[randint(0, len(characters)-1)]

    if input_field_type == UserDetails.EMAIL:
        # if there is a . or _ in the first or last position, remove it
        if user_detail[0] in [".", "_"]:
            user_detail = user_detail[1:]
        if user_detail[-1] in [".", "_"]:
            user_detail = user_detail[0:-1]
        user_detail += "@example.com"

    return user_detail

def create_user_data():

    username = random_user_details(UserDetails.USERNAME)
    password = random_user_details(UserDetails.PASSWORD)
    email = random_user_details(UserDetails.EMAIL)
    user_data = {
        "username": username,
        "email": email, 
        "password": password
        }
    return user_data

def create_temporary_user():

    username, email, password = create_user_data()
    get_user_model().objects.create_user(username, email, password)

    return username, email, password

def create_new_task_data():
        return {
            "title": "Task Title",
            "due_date": date(2050, 1, 1),
            "description" : "Task description"
        }

def create_task(username):

    task_data = create_new_task_data()
    user = get_user_model().objects.filter(username=username)

    new_task = Task(title=task_data["title"], due_date=task_data["due_date"])
    new_task.save()

    new_task_history = TaskHistory(
        status="U",
        task=new_task, 
        created_by=user
    )
    new_task_history.save()

    new_task_note = TaskNote(
        description=task_data["description"], 
        task=new_task, 
        created_by=user
    )
    new_task_note.save()
