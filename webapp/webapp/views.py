from django.shortcuts import render

def goHome(request):
    return render(request, "index.html")
