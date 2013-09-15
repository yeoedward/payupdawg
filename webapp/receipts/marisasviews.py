from django.http import HttpResponse
import receipts.models
import itertools 

def get_groups(user_id):
    return Homies.objects.filter(dawgs_equals=user_id)

def current_receipts(user_id):
    r = Receipts.objects.filter(owner_equals=user_id)

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

def networth(request, user_id):

    for i in current_receipts(user_id):
        if (i.owner=user_id):
            Dawg.objects.get(dawgs_equals=user_id).owes_you += i.price
        else:
            sum = 0

            #doesn't deal with mutual friends 
            for x in i.groups:
                sum += len(x)

            Dawg.objects.get(dawgs_equals=user_id).you_owe -= (i.price)/x

    return HttpResponse(Dawg.objects.get(dawgs_equals=user_id).owes_you - Dawg.objects.get(dawgs_equals=user_id).you_owe)

def permutations(a):
    # returns a list of all permutations of the list a
    if (len(a) == 0):
        return [[]]
    else:
        allPerms = [ ]
        for subPermutation in permutations(a[1:]):
            for i in xrange(len(subPermutation)+1):
                allPerms += [subPermutation[:i] + [a[0]] + subPermutation[i:]]
        return allPerms

def leastTransactions(request):
    u = (list)Users.objects
    debt = []
    collect = []

    for i in u:
        if (i.owes_you - i.you_owe < 0):
            debt.append(i)
        elif (i.owes_you - i.you_owe > 0):
            collect.append(i)

    debtPerm = permutations(debt)
    collectPerm = permuations(collect)



    return
