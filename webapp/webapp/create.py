from django.contrib import auth
from django.contrib.auth.models import User

user = User.objects.create_user(username='Niki',email='nikitam8@gmail.com', '123456')

print user.id
