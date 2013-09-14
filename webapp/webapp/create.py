from django.contrib import auth
from django.contrib.auth.models import User

user = User.objects.create_user(username='Niki',password='123456')

print user.get_username()
