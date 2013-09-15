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
    return HttpResponseRedirect("dashboard")
  else:
    return HttpResponseRedirect("invalid")

def logout(request):
  auth.logout(request) 
  return HttpResponseRedirect("/")

def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      return HttpResponseRedirect("dashboard")
  else:
    form = UserCreationForm()
  return render(request, "register.html", {'form': form})

def dashboard(request):
  return render(request, 'dashboard.html')

def about(request):
  return render(request, 'about.html')
