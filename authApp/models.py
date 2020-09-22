from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from scrapper.models import Product

class User(AbstractUser):
    username = models.CharField(blank=True, null=True,max_length=20)
    email = models.EmailField(_('email address'), unique=True)
    mobile=models.CharField(null=False,unique=True,max_length=10)

    # no email would be asked in login creds instead of username
    USERNAME_FIELD = 'email'
    # these feilds would be asked when creating superuser and + password which is mentioned in abstractuser
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=20,blank=True)
    dob = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=255,blank=True)
    country = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    zip = models.CharField(max_length=9,blank=True)
    photo = models.ImageField(upload_to='uploads',null=True, blank=True)

class Cart(models.Model):
    # cart would be either shopping cart or wish list cart
    cartChoice=(
        ('Shopping Cart','Shopping Cart'),
        ('wishList','wishList')
    )
    # user can have two types of card thus foreign key
    cart_type=models.CharField(max_length=20,choices=cartChoice,null=False) 
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.user.first_name +"'s "+self.cart_type

class CartItem(models.Model):
    # each card item would be a product with some count, so one to one field
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=False)
    quantity = models.IntegerField(default=1)
    # a cart can have many cartItems thus each cartItem maintain record to which cart it belongs, and if cart is deleted all the items in it would also be deleted
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)

    each_price=models.FloatField(blank=False)
    total_price = models.FloatField(blank=False,default=each_price)

    def __str__(self):
        return  self.cart.user.first_name +"'s "+self.cart.cart_type + " 's "+self.product.name
    