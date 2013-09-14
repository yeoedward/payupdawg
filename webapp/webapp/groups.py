from django.db import models

class Groups(models.Model):
     admin = models.CharField(max_length=30)
     members = models.ListField()            
            
        
