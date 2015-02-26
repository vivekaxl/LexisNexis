from django.db import models

# Create your models here.
class Registration(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    
   

def __str__(self):              # __unicode__ on Python 2
        return self.first_name
