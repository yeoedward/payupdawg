from django.http import HttpResponse
import receipts.models
import itertools 

def get_groups(user_id):
    return Homies.objects.filter(dawgs_equals=user_id)

def current_receipts(user_id):
    r = Receipts.objects.filter(owner_equals=user_id)
    find_groups = get_groups(user_id)
    for x in find_groups:
        r = chain(r, Receipts.objects.filter(homies_equals=x.name))

def receipts(request, user_id):
    html = list(current_receipts(user_id))
    return HttpResponse(html)

def balance(request, user_id):
    bal = 0

    for i in current_receipts(user_id):
        if (i.owner=user_id):
            bal += i.price
        else:
            bal -= (i.price)/(len(i.group))

    return HttpResponse(bal)
