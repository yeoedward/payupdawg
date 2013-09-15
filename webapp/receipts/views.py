from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from receipts.models import *

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


# populate table in request page

#TODO: doesn't work, filter receipts
def receipts(request):
#  def username(receipt):
#    receipt.owner = receipt.owner.all()[0].username
#    return receipt
  receipt_list = list(Receipt.objects.filter(owner__username=request.user.username))
  group_list = list(Homies.objects.filter(dawgs__username__exact=
                                            request.user.username))
  #receipt_list= map(username, receipt_list)
  return render(request, "receipts.html", {'group_list' : group_list, 
                          'receipt_list' : receipt_list})
# create new receipt
def newreceipt(request):
  title = request.POST.get('title')
  date = request.POST.get('date')
  totalPrice = request.POST.get('totalPrice')
  category = request.POST.get('category')
  owner = Dawg.objects.get(username=request.user.username)
  groups = Homies.objects.get(id=request.POST.get('groups'))
  r = Receipt(title=title, date=date, totalPrice=totalPrice, category=category)
  r.save()
  r.owner.add(owner)
  r.groups.add(groups)
  r.save()
  return HttpResponseRedirect("receipts")

def groups(request):
  group_list = list(Homies.objects.filter(dawgs__username__exact=
                                            request.user.username))
  return render(request, "groups.html", {'group_list' : group_list})

def group(request,group_id):
  g = Homies.objects.get(id = group_id)
  receipt_list = Receipt.objects.filter(groups__id__exact = group_id).order_by('-date')


  costdict = { }
  sum = 0.0
  for r in receipt_list:
    sum = sum + r.totalPrice
    temp = r.owner.all()[0].username
    if temp in costdict:
      costdict[temp] += r.totalPrice
    else:
      costdict[temp] = r.totalPrice

  peopleList = costdict.items()

  peopleL = []
  for x in peopleList:
    peopleL += [x]

  avg = sum / g.dawgs.count()
  people = map(lambda x: x.username,list(g.dawgs.all()))

  for p in people:
    if (p not in map(lambda (x,_): x, peopleL)):
      peopleL += [(p,0.0)]
  peopleL.sort(key=lambda (_,x): x)

  owners = map(lambda r: r.owner.all()[0].username, receipt_list)

  return render(request, "group.html", {'avg' : avg, 'people' : peopleL, 'zipped' : zip(receipt_list,owners)} )
