import random
from mainsite.models import *

# create group members
peeps = ['marisa','linda','kevin','li','stephen','niki','eddy']
 
def newDawg(name):
  d = Dawg(username=name)
  d.save()
  return d

dawgs = map(newDawg,  peeps)

# create group and add members
g = Homies(name = "fairfax annex")
g.save()
map(g.dawgs.add, dawgs)
g.save()

# create receipts
def genReceipts(user):
  for i in xrange(0,6,2):
    r = Receipt(title='Lotus'+str(i), date='2013-08-'+str(20+i),
                totalPrice=str(random.randint(1,10000)),
                category='Food'+str(i))
    r.save()
    r.owner.add(user)
    r.groups.add(g)
    r.save()

map (genReceipts, dawgs)
