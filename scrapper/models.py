from django.db import models

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=50, blank=False, default='')
    rating=models.CharField(max_length=3, blank=False, default='')
    image_url=models.CharField(max_length=200, blank=False, default='')
    # price=models.DecimalField(blank=False,max_digits=19, decimal_places=10)
    price=models.CharField(max_length=10, blank=False, default='NA')
