from django.db import models

class Receipt(models.Model):
    #have user-defined categories too..add in later
    CATEGORY = ('FOOD', 'SUPPLIES', 'DRINKS', 'OTHER')
    
    name = models.CharField(max_length = 30)
    date = models.DateField()
    #category = models.ListField(choices=CATEGORY)
    price = models.FloatField(default=0.00)
    
    #permissions
    user = models.CharField(max_length = 100)
    #groups = models.ListField()

