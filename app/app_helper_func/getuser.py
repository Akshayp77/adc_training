from django.contrib.auth import tokens
from rest_framework.authtoken.models import Token

def get_user(value):
    '''This function returns user id and take token as an argument.
    '''
    user_id = Token.objects.get(key=value).user_id
    return user_id