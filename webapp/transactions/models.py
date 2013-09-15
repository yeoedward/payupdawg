from django.db import models

# Create your models here.

class transactions(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField()
    price = models.FloatField(default=0.00)
    category = models.CharField(max_length=30)
    
    #shared is a list of members
    # NEED TO EDIT shared = models.ListField()
    owner = models.CharField(max_length=30)

