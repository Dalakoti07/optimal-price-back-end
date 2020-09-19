from rest_framework import serializers
from .models import User, UserProfile,CartItem,Cart
import math

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        # customize the fields count and name u want to be exposed via json api
        fields = ('title', 'dob', 'address', 'country', 'city', 'zip', 'photo')

class UserSerializerWithoutPassword(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'profile')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name','password', 'last_name', 'profile')
        # Note the the password field is set as a write_only field. 
        # Meaning that it will be used for deserialization(creating the model) but not for serialization.
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        # customize the fields count and name u want to be exposed via json api
        fields = ('id','cart_type','product_image','each_price','product_id', 'product_name', 'quantity', 'total_price')
        
    product_image=serializers.CharField(source='product.image_url')
    product_name=serializers.CharField(source='product.name')
    product_id=serializers.UUIDField(source='product.id')
    cart_type=serializers.CharField(source='cart.cart_type')
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,obj):
        return obj.quantity * obj.each_price

