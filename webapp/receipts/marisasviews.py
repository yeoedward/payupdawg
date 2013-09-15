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
    a = []

    for i in current_receipts(user_id):
        for x, y in [i]:
            if a.count(i.user) == 0:
                a.append(i.user, -1*i.price)
            else:
                y = y - i.price

    for u, p in a:
        if u == user_id:
            p = -1*p

    return HttpResponse(html)
