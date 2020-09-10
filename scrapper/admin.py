from django.contrib import admin

# Register your models here.
from .models import Product,Deals

admin.site.register(Product)
admin.site.register(Deals)