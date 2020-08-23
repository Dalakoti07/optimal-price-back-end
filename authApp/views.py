from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer

# Also add these imports
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add this code block
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
