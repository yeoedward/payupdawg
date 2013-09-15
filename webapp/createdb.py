from receipts.models import *
d = Dawg(username="eddy")
d.save()
g = Homies(name="annex")
g.save()
g.dawgs.add(d)
g.save()
