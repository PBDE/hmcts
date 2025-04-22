from string import ascii_letters, digits, punctuation
from random import randint
from django.contrib.auth import get_user_model

from case_management.enums import UserDetails

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


