from django.http import HttpResponse
from receipts.models import Receipts, Dawg, Homies

def homies(request, user_id):
    your_groups = Homies.objects.filter(dawg=user_id)
    #your_groups = Homies.objects.get(dawgs__contains=user_id)
    return HttpResponse()
