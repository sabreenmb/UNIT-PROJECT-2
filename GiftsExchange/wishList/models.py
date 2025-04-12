from django.db import models

# Create your models here.


class Item(models.Model):
    
    name = models.CharField(max_length=1024)
    image=models.ImageField(upload_to="images/" , null=True)
    price =models.IntegerField(null=True )
