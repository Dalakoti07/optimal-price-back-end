from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', obtain_jwt_token),
]