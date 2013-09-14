from django.shortcuts import render
from django.contrib import auth

def goHome(request):
  username = request.POST.get('username', '')
  password = request.POST.get('password', '')
  user = auth.authenticate(username=username, password=password)
  if user is not None and user.is_active:
    auth.login(request, user)
    return HttpResponseRedirect("/account/loggedin/")
  else:
    return HttpResponseRedirect("/account/invalid/")
