from django.db import models

# Create your models here.


class Item(models.Model):
    
    name = models.CharField(max_length=1024)
    image=models.ImageField(upload_to="images/" , null=True)
    price =models.IntegerField(null=True )



class Gift(models.Model):
    name = models.CharField(max_length=1024)
    age = models.CharField(max_length=1024)
    image=models.ImageField(upload_to="images/" , null=True)
    price =models.IntegerField(null=True )
    link = models.URLField(max_length=200, blank=True, null=True)  


