from django.conf.urls import url, include
from rest_framework import routers
# from .views import ProductViewSet
from scrapper import views

# router = routers.DefaultRouter()
# router.register(r'products', )

urlpatterns = [
    url(r'^search_in_db',views.search_in_db),
    url(r'^scrap', views.search_by_scrap),
    url(r'^',views.viewAllProducts),
]