from rest_framework import serializers
from .models import Product,Deals

# TODO make a hyperlink or detail url in each product it may be null
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'rating', 'image_url', 'price','amazon_link','flipkart_link','created_at','brand_name','ecommerce_company','details']

class DealsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Deals
        fields = ['sales_link','sales_image_link']