import requests
from django.core.files import File
from urllib import request
import os

def save_user_profile(backend, user, response, *args, **kwargs):
    access_token=response['access_token']

    response = requests.get(
        f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}' 
    )

    data = response.json()

    print(f'{data=}')

    user.email = data['email']

    user.first_name = data['given_name']

    user.save()