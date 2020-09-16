from django.conf.urls import url, include
from rest_framework import routers
from scrapper import views
from .views import ReviewViewSet,ProductsViewSet,ProductDetailViewSet,ProductFullSpecViewSet,LatestMobilesViewSet,ecommerceBasedSearchViewSet

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
urlpatterns = [
    url(r'^search',product_list, name='search-list'),
    url(r'^scrap', views.search_by_scrap),
    url(r'^deals',views.fetchTheDeals),
    url(r'^product_details/(?P<productId>[\w-]*)', product_detail_list, name='product-detail'),
    url(r'^products', product_list, name='product-list'),
    url(r'^reviews/(?P<productId>[\w-]*)', reviews_list, name='review-detail'),
    url(r'^full_specs/(?P<productId>[\w-]*)',product_full_spec,name='full-spec-detail'),
    url(r'^latest_mobiles/',LatestMobilesViewSet.as_view({
        'get':'list',
    })),
    url(r'^site',ecommerceBasedSearchViewSet.as_view({
        'get':'list',
    })),
]

# urlpatterns += router.urls