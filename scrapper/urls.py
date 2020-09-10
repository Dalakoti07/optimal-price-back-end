from django.conf.urls import url, include
from rest_framework import routers
# from .views import ProductViewSet
from scrapper import views

# router = routers.DefaultRouter()
# router.register(r'products', )
#TODO combine all the search query in one url, and allows various paramters like search by category and the  search by company and search by name substring
urlpatterns = [
    url(r'^search_in_db',views.search_in_db),
    url(r'^scrap', views.search_by_scrap),
    url(r'^search',views.searchByCategory),
    url(r'^deals',views.fetchTheDeals),
    url(r'^',views.viewAllProducts),
]