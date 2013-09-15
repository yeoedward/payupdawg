from django.db import models

# Create your models here.

#for member-group relationships
class Dawg(models.Model):
    name = models.CharField(max_length=30)
    budget = models.FloatField(default=0.00)
    owe_you = models.FloatFied(default=0.00) 
    you_owe = models.FloatField(default=0.00)

class Homies(models.Model):
    name = models.CharField(max_length=30)
    dawgs = models.ManyToManyField(Dawg)

class Receipt(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField()
    price = models.FloatField(default=0.00)
    category = models.CharField(max_length=30)

    owner = models.ManyToManyField(Dawg)
    groups = models.ManyToManyField(Homies)

