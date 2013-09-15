from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
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

def matchmake(L):
  if L is None: return None
  (result,trans) = del_eql(L)
  if len(result) == 0: return result + trans
  assert(len(result) > 1)
  (n1,m1) = result.pop()
  (n2,m2) = result.pop(0)
  new_n = n1 + n2
  new_m = m1 if abs(n1) >= abs(n2) else m2
  changed_hands = min(abs(n1),abs(n2))
  payer = m1 if n1 > 0 else m2
  payee = m2 if n1 > 0 else m1
  return trans + [(payer,payee,changed_hands)] + matchmake(insert((new_n,new_m),result))


def stringify(L):
  if L is None: return None
  return map(lambda (a,b,n): a+" pays $"+str(n)+" to "+b+".", L)


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
  zipped = zip(receipt_list, owners)

  net_spend = sorted(map(lambda (o,r): (avg-r, o), peopleL), key = lambda (n,_): n)
  try:
    transactions = stringify(matchmake(net_spend))
  except Exception:
    transactions = None
  return render(request, "group.html", {'avg' : avg, 'people' : peopleL, 'zipped' : zipped,
                                        'gid' : group_id, 'trans' : transactions} )

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
  
