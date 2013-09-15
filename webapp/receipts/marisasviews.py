from django.http import HttpResponse
import receipts.models
import itertools 

def my_receipts(user_id):
    return Receipts.objects.filter(owner_equals=user_id)

def other_receipts(user_id):
    r = []
    find_groups = get_groups(user_id)
    for x in find_groups:
        r = chain(r, Receipts.objects.filter(homies_equals=x.name))
    return r

def get_groups(user_id):
    return Homies.objects.filter(dawgs_equals=user_id)

def current_receipts(user_id):
    return chain(my_receipts, other_receipts)

def receipts(request, user_id):
    html = list(current_receipts(user_id))
    return HttpResponse(html)

