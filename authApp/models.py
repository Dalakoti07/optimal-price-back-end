from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(blank=True, null=True,max_length=20)
    email = models.EmailField(_('email address'), unique=True)

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

