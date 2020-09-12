from django.contrib import admin

# Register your models here.
from .models import Product,Deals,ProductDetail,Review

admin.site.register(Product)
admin.site.register(Deals)
admin.site.register(ProductDetail)
admin.site.register(Review)