from django.http import HttpResponse
from receipts.models import Receipts, Dawg, Homies
from itertools import chain

def current_receipts(request, user_id):
    r = Receipts.objects.filter(owner_equals=user_id)

    find_groups = Homies.objects.filter(dawgs_equals=user_id)
    for x in find_groups:
        r = chain(r, Receipts.objects.filter(homies_equals=x.name))

    return HttpResponse(r)


