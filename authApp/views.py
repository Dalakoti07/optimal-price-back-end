from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer

# Also add these imports
from .permissions import IsLoggedInUserOrAdmin, IsAdminUser
from rest_framework.permissions import AllowAny

from rest_framework_jwt.settings import api_settings
from .customJWTUtils import jwt_payload_handler

jwt_payload_handler = jwt_payload_handler
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
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
        # self.perform_create(serializer)
        savedInstance=serializer.save()
        print("saved instance is ",savedInstance)
        payload = jwt_payload_handler(savedInstance)
        token = jwt_encode_handler(payload)
        return Response({'user':serializer.data,'token':token}, status=status.HTTP_201_CREATED)