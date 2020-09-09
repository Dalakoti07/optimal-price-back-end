from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'rating', 'image_url', 'price','amazon_link','flipkart_link','created_at','brand_name','ecommerce_company']
