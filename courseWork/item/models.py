from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(max_length=20)
    shelfLife = models.BooleanField()
   
    def __str__(self):
        return self.name  

    @property
    def shL(self):
        temp = "Doesnt' have shelf life"
        if(self.shelfLife):
            temp = "Does have sehlf life"
        return temp


class Order(models.Model):
    num = models.CharField(max_length=20)
    date = models.DateField()
    items = models.ManyToManyField(Item)
   
    def __str__(self):
        return self.num 

   

