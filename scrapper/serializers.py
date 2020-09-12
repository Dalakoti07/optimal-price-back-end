from rest_framework import serializers
from .models import Product,Deals,ProductDetail,Review
import json

# TODO make a hyperlink or detail url in each product it may be null
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'rating', 'image_url', 'price','amazon_link','flipkart_link','created_at','brand_name','ecommerce_company']

class DealsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Deals
        fields = ['sales_link','sales_image_link']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model =Review
        fields = '__all__'

class JSONField(serializers.Field):
    def to_representation(self, obj):
        return json.loads(obj)

    def to_internal_value(self, data):
        return json.dumps(data)

class ProductDetailSerializer(serializers.ModelSerializer):
    product_full_spec =JSONField()

    class Meta:
        model=ProductDetail
        fields = ['product_full_spec','product_images','product']
    
    def detail_getter(self,obj):
        return obj.product_full_spec