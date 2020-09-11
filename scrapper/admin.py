from django.contrib import admin

# Register your models here.
from .models import Product,Deals,ProductDetails,Review

admin.site.register(Product)
admin.site.register(Deals)
admin.site.register(ProductDetails)
admin.site.register(Review)