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

def networth(request, user_id):

    for i in current_receipts(user_id):
        if (i.owner=user_id):
            Dawg.objects.get(dawgs_equals=user_id).owes_you += i.price
        else:
            sum = 0

            #assumes disjoint
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

def payments(dList, cList, answer):
    if (len(cList) == 0):
        return []
    else:
        #net
        d = dList[0][1]
        c = cList[0][1]

        #debtor owes more money
        if (d + c < 0): 
            dList[0][1] = d + c
            return [dList[0][0] + "pays" + cList[0][0] + "in full \n"] + payments(dList, cList[1:]]
        #exact amount owed 
        elif (d - c == 0):
            return [dList[0][0] + "pays" + cList[0][0] + "in full \n"] + payments(dList[1:], cList[1:]]
        #collector needs more
        else:
            cList[0][1] = d + c
            return [dList[0][0] + "pays" + cList[0][0] + "in full \n"] + payments(dList[1:], cList]


def leastTransactions(request):
    u = (list)Users.objects
    debt = []
    collect = []
    total = []
    cNet = []
    dNet = []

    #sorts
    for i in u:
        if (i.owes_you - i.you_owe < 0):
            debt.append([i.name, i.owes_you-i.you_owe])
        elif (i.owes_you - i.you_owe > 0):
            collect.append([i.name, i.owes_you-i.you_owe])

    debtPerm = permutations(debt)
    collectPerm = permuations(collect)

    for d in debtPerm:
        for c in collectPerm:
            total +=payments


    #might not be always working, is there always a total[0]?
    sum = len(total[0])
    answer = []
    for t in total:
        if len(t) < sum:
            answer = t
            sum = len(t)

    return answer
