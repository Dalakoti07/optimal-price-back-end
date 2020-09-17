from rest_framework import serializers
from .models import Product,Deals,ProductDetail,Review
import json

# TODO make a hyperlink or detail url in each product it may be null
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','product_category', 'rating', 'image_url', 'flipkart_price'
                    ,'amazon_price','amazon_link','flipkart_link','created_at','brand_name','ecommerce_company']

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

class SUBJSONField(serializers.Field):
    def to_representation(self, obj):
        complete_json= json.loads(obj)
        try:
            sub_json=complete_json['General']
            return sub_json
        except Exception as e:
            return {}

    def to_internal_value(self, data):
        return json.dumps(data)

class ProductFullSpecsSerializer(serializers.ModelSerializer):
    product_full_spec =JSONField()

    class Meta:
        model=ProductDetail
        fields = ['product','product_full_spec']
    
    def detail_getter(self,obj):
        return obj.product_full_spec

class ProductDetailsSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'rating', 'image_url', 'amazon_price','flipkart_price','amazon_link',
                    'flipkart_link','created_at','brand_name','ecommerce_company',
                    'image_urls','general_features']

    image_urls = JSONField(source='details.product_images')
    general_features = SUBJSONField(source='details.product_full_spec')
