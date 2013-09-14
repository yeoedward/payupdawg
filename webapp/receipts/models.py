from django.db import models

# Create your models here.

class Receipt(models.Model):
    title = 
    date = models.DateField()
    category = models.CharField(max_length=30)
    #shared is a list of members
    shared = models.DataList()
    owner = models.CharField(max_length=30)

