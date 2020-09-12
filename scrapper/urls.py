from django.conf.urls import url, include
from rest_framework import routers
from scrapper import views
from .views import ReviewViewSet,ProductsViewSet,ProductDetailViewSet,ProductFullSpecViewSet

router = routers.SimpleRouter() 

product_full_spec=ProductFullSpecViewSet.as_view({
    'get':'list',
})

reviews_list=ReviewViewSet.as_view({
    'get':'list',
})
product_list=ProductsViewSet.as_view({
    'get':'list',
})
product_detail_list=ProductDetailViewSet.as_view({
    'get':'list',
})

# router = routers.DefaultRouter()
# router.register(r'products', )
# TODO make productdetails feilds as read only when viewed through django
#TODO combine all the search query in one url, and allows various paramters like search by category and the  search by company and search by name substring
urlpatterns = [
    url(r'^search',product_list, name='search-list'),
    url(r'^scrap', views.search_by_scrap),
    url(r'^deals',views.fetchTheDeals),
    url(r'^product_details', product_detail_list, name='product-detail'),
    url(r'^get_product_detail',views.getTheProductDetails),
    url(r'^products', product_list, name='product-list'),
    url(r'^reviews/(?P<productId>[\w-]*)', reviews_list, name='review-detail'),
    url(r'^full_specs/(?P<productId>[\w-]*)',product_full_spec,name='full-spec-detail'),
]

# urlpatterns += router.urls