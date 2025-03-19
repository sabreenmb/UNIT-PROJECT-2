from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    class GenderChoices(models.TextChoices):
        F= 'Female' , 'F'
        M= 'Male', 'M'
        NS='Not Specified','NS'
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True ,unique=True)
    gender=models.CharField(choices=GenderChoices.choices ,max_length=128 ,default=GenderChoices.NS)
    birth_date=models.DateField(blank=True ,null=True)  


    
