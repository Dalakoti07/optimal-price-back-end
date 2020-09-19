from django.shortcuts import render
import jwt
# Create your views here.
from rest_framework import viewsets

from scrapper.models import Product
from .models import User,CartItem,Cart
from .serializers import UserSerializer,UserProfileSerializer,CartItemSerializer,UserSerializerWithoutPassword
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from django.db.utils import IntegrityError

# Also add these imports
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.permissions import AllowAny

from rest_framework_jwt.settings import api_settings
from .customJWTUtils import jwt_payload_handler

jwt_payload_handler = jwt_payload_handler
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
from rest_framework.response import Response
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    username=User.username
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        # anyone can create account
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            # a user can see his details, and update his own details, or either user can do this
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            # only admin can view all users and delete a user
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        savedInstance=serializer.save()
        # print("saved instance is ",savedInstance)
        payload = jwt_payload_handler(savedInstance)
        token = jwt_encode_handler(payload)
        # create user's wishlist and shopping list cart
        shoppingCart=Cart(cart_type='Shopping Cart',user=savedInstance)
        wishList=Cart(cart_type='wishList',user=savedInstance)
        shoppingCart.save()
        wishList.save()

        return Response({'token':token,'user':serializer.data}, status=status.HTTP_201_CREATED)

def getUserModelFromToken(auth_header):
    # parse the token
    token=auth_header.split(' ')[1]
    decoded_token=jwt_decode_handler(token)
    # print('decode ',decoded_token)
    userId=decoded_token['user_id']
    return User.objects.get(id=userId)
    

@api_view(['GET','POST','PUT'])
def cartAPI(request):
    cart_type=request.GET['type']
    auth_header=request.META['HTTP_AUTHORIZATION'] 
    
    if cart_type=='Shopping Cart' or cart_type=='wishList':
        if request.method=='GET':
            user=getUserModelFromToken(auth_header=auth_header)
            nested_cart=Cart.objects.all().filter(cart_type=cart_type,user=user)
            if len(nested_cart)==1:
                nested_cart=nested_cart[0]
                allItems=CartItem.objects.all().filter(cart=nested_cart)
                return Response(CartItemSerializer(allItems,many=True).data)
            else:
                return Response('we could not found any cart items')

        elif request.method=='POST':
            # add a product to cart        
        
            user=getUserModelFromToken(auth_header=auth_header)
            nested_cart=Cart.objects.all().filter(cart_type=cart_type,user=user)[0]

            productInfo=request.data
            # find product
            product=Product.objects.get(id=productInfo['product_id'])
            each_price=-1
            if product.amazon_price and product.flipkart_price:
                each_price=min(product.amazon_price,product.flipkart_price)
            elif product.amazon_price:
                each_price=product.amazon_price
            elif product.flipkart_price:
                each_price=product.flipkart_price

            # each price would be calculated at model end
            ifThisExist=CartItem.objects.all().filter(product=product,cart=nested_cart)
            print('len ',len(ifThisExist))
            if len(ifThisExist)>=1:
                return Response({"message":"this item is already in your cart"},400)
            else:
                newCartItem=CartItem(product=product,quantity=1,cart=nested_cart,each_price=each_price,total_price=each_price)
                newCartItem.save()
                return Response(CartItemSerializer(newCartItem,many=False).data)
            
        elif request.method=='PUT':

            updateCartItemInfo=request.data
            itemId=updateCartItemInfo['item_id']
            itemCount=int(updateCartItemInfo['count'])
            try:
                item=CartItem.objects.get(id=itemId)
                if request.user == item.cart.user:
                    item.quantity=itemCount
                    item.save()
                    return Response(CartItemSerializer(item,many=False).data)
                else:
                    return Response({'message': 'You are not authorizated'},status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                return Response({'message':'Invalid cart Id'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('wrong cart type',400)

@api_view(['GET','POST'])
def profileApi(request):
    auth_header=request.META['HTTP_AUTHORIZATION'] 

    if request.method=='GET':
        try:
            return Response(UserSerializer(getUserModelFromToken(auth_header)).data)
        except Exception as e:
            return Response({'message':'Invalid token'},status=400)
    elif request.method=='POST':
        updatedUserProfileData=request.data
        userObject=getUserModelFromToken(auth_header)
        serializer=UserSerializerWithoutPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # basic user creds update
            userObject.email=request.data['email']
            userObject.first_name=request.data['first_name']
            userObject.last_name=request.data['last_name']
            userObject.save()
            # update the user profile
            userObject.profile.title=request.data['profile']['title']
            userObject.profile.dob=request.data['profile']['dob']
            userObject.profile.address=request.data['profile']['address']
            userObject.profile.country=request.data['profile']['country']
            userObject.profile.city=request.data['profile']['city']
            userObject.profile.zip=request.data['profile']['zip']
            userObject.profile.photo=request.data['profile']['photo']
            userObject.profile.save()
            # generate new user token, and send it to user
            payload = jwt_payload_handler(userObject)
            token = jwt_encode_handler(payload)
            # Response({'token':token,'user':serializer.data}, status=status.HTTP_201_CREATED)
            return Response( {'token':token,'user':UserSerializer(userObject).data},200)
        else:
            return Response({'message':'invalid data'},status=400)