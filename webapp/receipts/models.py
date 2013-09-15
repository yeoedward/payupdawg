from django.db import models

# Create your models here.

#for member-group relationships
class Dawg(models.Model):
    username = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    budget = models.FloatField(default=0.00)
    owe_you = models.FloatField(default=0.00) 
    you_owe = models.FloatField(default=0.00)
    # pic = models.ImageField()

    def __unicode__(self):
        return self.username

class Homies(models.Model):
    name = models.CharField(max_length=30)
    dawgs = models.ManyToManyField(Dawg)

    def __unicode__(self):
        return self.name

class Receipt(models.Model):
    title = models.CharField(max_length=30)
    date = models.DateField()
    totalPrice = models.FloatField(default=0.00)
    indPrice = models.FloatField(default=0.00)
    category = models.CharField(max_length=30)

    owner = models.CharField(max_length=30)
    groups = models.ManyToManyField(Homies)
    
    def __unicode__(self):
        return self.title


