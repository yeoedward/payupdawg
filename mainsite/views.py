from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from mainsite.models import *

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
      username = request.POST.get('username')
      d = Dawg(username=username)
      d.save()
      password = request.POST.get('password1')
      user = auth.authenticate(username=username, password=password)
      if user is not None and user.is_active:
        auth.login(request,user)
      return HttpResponseRedirect("dashboard")
  else:
    form = UserCreationForm()
  return render(request, "register.html", {'form': form})

def dashboard(request):
  return render(request, 'dashboard.html')

def about(request):
  return render(request, 'about.html')

def invalid(request):
  return render(request, 'invalid.html')


# populate table in request page

def receipts(request):
#  def username(receipt):
#    receipt.owner = receipt.owner.all()[0].username
#    return receipt
  receipt_list = list(Receipt.objects.filter(owner__username = 
                                             request.user.username)
                                     .order_by('-date'))

  # convert cents to dollars
  def f(x):
    x.totalPrice /= 100.0
    return x
  receipt_list = map(f, receipt_list)

  group_list = list(Homies.objects.filter(dawgs__username__exact=
                                            request.user.username))
  #receipt_list= map(username, receipt_list)
  return render(request, "receipts.html", {'group_list' : group_list, 
                          'receipt_list' : receipt_list})
# create new receipt
def newreceipt(request):
  title = request.POST.get('title')
  date = request.POST.get('date')

  # convert dollars to cents
  totalPrice = float(request.POST.get('totalPrice')) * 100

  category = request.POST.get('category')
  owner = Dawg.objects.get(username=request.user.username)
  try:
    groups = Homies.objects.get(id=request.POST.get('groups'))
    r = Receipt(title=title, date=date, totalPrice=totalPrice, category=category)
    r.save()
    r.owner.add(owner)
    r.groups.add(groups)
    r.save()
  except ValidationError:
    pass
  return HttpResponseRedirect("receipts")

def groups(request):
  group_list = list(Homies.objects.filter(dawgs__username__exact=
                                            request.user.username))
  return render(request, "groups.html", {'group_list' : group_list})

# insert tuple into list of tuples, ordered by the first element
def insert((x,m),L):
  if L == []:
    return [(x,m)]
  (a,m2) = L.pop(0)
  if x <= a:
    return [(x,m),(a,m2)]+L
  return [(a,m2)] + insert((x,m),L)

def del_eql(L):
  trans = []
  to_del = set()
  S = {}
  for (i,(n,m)) in enumerate(L):
    if n == 0:
      to_del.add(i)
    if -n in S:
      to_del.add(S[-n][0])
      to_del.add(i)
      payer = m if i > S[-n][0] else S[-n][1]
      payee = S[-n][1] if i > S[-n][0] else m
      trans += [(m,S[-n][1],abs(n))]
      del S[-n]
    else:
      S[n] = (i,m)
  result = []
  for (i,p) in enumerate(L):
    if i in to_del:
      continue
    result += [p]
  return (result,trans)

# Wrapper function for matchmaker(). Converts amount spent to a net value w.r.t # avg, sorts the list by amount, and then calls matchmaker
def matchmake(L, avg):
  netSpendList = sorted(map(lambda (o,r): (avg - r, o), L), 
                        key = lambda (n,_): n)
  return matchmaker(netSpendList)

# Matches up people with eql amts they owe/are owed.
# Matches up people who owe or are owed the largest amts
# Repeat until everyone has settled debts
def matchmaker(L):
  if L == []: return []
  (result,trans) = del_eql(L)
  if len(result) == 0: return trans 
  if len(result) == 1:
    # rounding error. Someone will lose money.
    assert(result[0][0] < 0)
    return trans + result
  (n1,m1) = result.pop()
  (n2,m2) = result.pop(0)
  new_n = n1 + n2
  new_m = m1 if abs(n1) >= abs(n2) else m2
  changed_hands = min(abs(n1),abs(n2))
  payer = m1 if n1 > 0 else m2
  payee = m2 if n1 > 0 else m1
  return trans + [(payer,payee,changed_hands)] + \
                 matchmaker(insert((new_n,new_m),result))


# Converts tuples into strings, with the amounts converted to dollars
def stringify(L):
  if L is None: return None
  def strng(t):
    if len(t) == 2:
      (amt, per) = t
      return per+" loses "+str(-amt/100.0)+"."
    else:
      (a,b,n) = t
      return a+" pays $"+str(n/100.0)+" to "+b+"."
  return map(strng, L)

def group(request,group_id):
  g = Homies.objects.get(id = group_id)
  receipt_list = Receipt.objects.filter(groups__id__exact = group_id)\
                                .order_by('-date')


  # compute average and generate list of people who paid
  costdict = { }
  total = 0
  for r in receipt_list:
    total += r.totalPrice
    temp = r.owner.all()[0].username
    if temp in costdict:
      costdict[temp] += r.totalPrice
    else:
      costdict[temp] = r.totalPrice

  avg = (total / g.dawgs.count())

  peopleWhoPaid = costdict.items()
  allPeople = map(lambda x: x.username,list(g.dawgs.all()))

  # Add those who did not pay into the list with $0 spending
  for p in allPeople:
    if p not in costdict:
      peopleWhoPaid += [(p,0)]

  # format it so template can easily extract data
  table = map(lambda r: (r, r.owner.all()[0].username, r.totalPrice/100.0), 
              receipt_list)

  transactions = stringify(matchmake(peopleWhoPaid, avg))

  # convert from cents to dollars
  peopleWhoPaid = map(lambda (p,x): (p, x/100.0), peopleWhoPaid)
  avg /= 100.0

  # sort the people who paid in ascending order of amt paid
  peopleWhoPaid = sorted(peopleWhoPaid, key = lambda (p,x): x)

  return render(request, "group.html", 
                {'avg' : avg, 'people' : peopleWhoPaid, 'table' : table,
                 'gid' : group_id, 'trans' : transactions})

def creategroup(request):
  name = request.POST.get('name')
  g = Homies(name = name)
  g.save()
  d = Dawg.objects.get(username=request.user.username)
  g.dawgs.add(d)
  g.save()
  return HttpResponseRedirect("groups")

def addfriend(request):
  newfriend = request.POST.get('username')
  gid = request.POST.get('gid')
  try:
    d = Dawg.objects.get(username=newfriend)
  except Exception:
    return HttpResponseRedirect("/group/"+gid)
  g = Homies.objects.get(id=gid)
  g.dawgs.add(d)
  g.save()
  return HttpResponseRedirect("/group/"+gid)
  
