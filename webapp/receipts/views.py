from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect

def goHome(request):
  return render(request, 'index.html')

def login(request):
  username = request.POST.get('username', '')
  password = request.POST.get('password', '')
  user = auth.authenticate(username=username, password=password)
  if user is not None and user.is_active:
    auth.login(request, user)
    return HttpResponseRedirect("/account/loggedin/")
  else:
    return HttpResponseRedirect("/account/invalid/")

def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      return HttpResponseRedirect("/books/")
  else:
    form = UserCreationForm()
  return render(request, "register.html", {'form': form})
