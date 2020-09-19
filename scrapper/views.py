from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer,DealsSerializer,ReviewSerializer,ProductDetailsSerilizer,ProductFullSpecsSerializer

# Create your views here.
from .models import Product,Deals,ProductDetail,Review
from django.http import HttpResponse, JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# utils function import
from .flipkartScrapper import scrapAPage as flipkartScrapAPage,scrapMultiplePages as flipkartScrapMultiplePage, scrapDeals as flipkartDeals
from .ScrapperUtils import serialiseTheScrappedPagesIntoCSV,mergeList,saveToDB,deserialiseTheListFromCSV,pseudoMergeIt,saveProductDetailsToDB,returnJsonResponseFromProductList
from .amazonScrapper import scrapAPage as amazonScrapAPage,scrapMultiplePages as amazonScrapMultiplePage
from .ProductDetailsScrapper import scrapTheDetails
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions

# selenium and web scrapping stuff
import argparse
import time
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
from rest_framework.decorators import api_view
from authApp.permissions import IsAdminUser,IsLoggedInUserOrAdmin
# use selenium service to avoid too much rersource usage
import sys 
from rest_framework.reverse import reverse
from rest_framework.response import Response

# make driver for getting all specs
productDetailsService = Service('./driver')
# FIXME uncommment them 
# productDetailsService.start()
# productDetailsdriver=webdriver.Remote(productDetailsService.service_url)
# TODO u can use read only viewset, that would be helpful https://www.django-rest-framework.org/api-guide/viewsets/


# TODO make the readable time stamp and then put that timestamp in each product and then query that back
@api_view(['GET'])
@permission_classes([IsAdminUser])
def search_by_scrap(request):
    if request.method=='GET':
        
        searchKey=str(request.GET['search'])
        pagesLimit=None
        try:
            pagesLimit=int(request.GET['pages'])
        except Exception as e:
            print(e)
        
        # start service of selenium and prepare the driver
        service = Service('./driver')
        service.start()
        driver=webdriver.Remote(service.service_url)

        if not pagesLimit:
            pagesLimit=5
        # start the time
        start_time = time.perf_counter()
        print('scrapping :{} with {} pages '.format(searchKey,pagesLimit))
        # scrap the data from flipkart 
        flipkartItems,category_type=flipkartScrapMultiplePage(driver,searchKey,pagesLimit)
        print("{} items scrapped from flipkart".format(len(flipkartItems)))
        serialiseTheScrappedPagesIntoCSV(flipkartItems,"./scrapper/csvs/flipkart-django-{}_pages-{}.csv".format(pagesLimit,searchKey))
        
        # launch a new tab,to run amazon and python query consequently

        # scrap the data from amazon
        # the category returned by amazon is last category so 
        amazonItems,category_type=amazonScrapMultiplePage(driver,searchKey,pagesLimit)
        print("{} items scrapped from amazon".format(len(amazonItems)))
        serialiseTheScrappedPagesIntoCSV(amazonItems,"./scrapper/csvs/amazon-django-{}_pages-{}.csv".format(pagesLimit,searchKey))

        elapsed_time = time.perf_counter() - start_time
        if category_type=='men fashion' or category_type=='women fashion' or category_type=='fashion':
            # merge is necessary so that it comes in right format, we pseudo merge in this case
            pseudoMergeAmazon=pseudoMergeIt(amazonItems,'amazon',category_type)
            pseudoMergeFlipkart=pseudoMergeIt(flipkartItems,'flipkart',category_type)
            saveToDB(pseudoMergeAmazon)
            saveToDB(pseudoMergeFlipkart)
            return JsonResponse(returnJsonResponseFromProductList(pseudoMergeAmazon+pseudoMergeFlipkart,totalTime=elapsed_time),safe=False)
        print(f"searched {searchKey} and got executed in {elapsed_time:0.2f} seconds.")
        if amazonItems and flipkartItems:
            # serialisedData=ProductSerializer(responseFromFunc,many=True)
            merged_list=mergeList(amazonList=amazonItems,flipkartList=flipkartItems,categoryType=category_type)
            # TODO pass the timestamp and then query that time stamp
            print('merged list size{} '.format(len(merged_list)))
            saveToDB(merged_list)
            return JsonResponse( returnJsonResponseFromProductList( merged_list,totalTime=elapsed_time),safe=False)
        else:
            return HttpResponse('Server Error')
        

        # unit testing for db
        # saveToDB(mergeList(deserialiseTheListFromCSV("./scrapper/csvs/flipkart-django-5_pages-samsung phones.csv"),deserialiseTheListFromCSV("./scrapper/csvs/amazon-django-5_pages-samsung phones.csv"),categoryType='mobiles'))
        # return JsonResponse('it should be done',safe=False)

# TODO convert to viewset
@api_view(['GET'])
def fetchTheDeals(request):
    if request.method=='GET':
        allDeals=Deals.objects.all()
        if len(allDeals)==0:
            # scrap new deals
            service = Service('./driver')
            service.start()
            driver=webdriver.Remote(service.service_url)
            deals= flipkartDeals(driver=driver,callFromMain=False)
            # TODO see if this does not close the product scrap service
            driver.close()
            if not deals:
                return HttpResponse('something broke')
            for key in deals:
                try:
                    deal = Deals(sales_link=deals[key]['href_link'],sales_image_link=deals[key]['image_url'])
                    deal.save()
                except Exception as e:
                    print('error in saving deal object {}'.format(e))
            # done
        else:
            serializer=DealsSerializer(allDeals,many=True,context={'request': request})
            return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponseBadRequest('Method Not allowed ')

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    def list(self,request,productId=None):
        if productId:
            print('searching reviews for product id '+productId)
            all_reviews=Review.objects.all().filter(product=productId)
            serializer = self.get_serializer(all_reviews, many=True)
            return Response(serializer.data)
        else:
            print('getting all reviews')
            all_reviews=Review.objects.all()
            serializer = self.get_serializer(all_reviews, many=True)
            return Response(serializer.data)

class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    def get_queryset(self):
        company = self.request.query_params.get('company')
        category= self.request.query_params.get('category')
        product_name_contains = self.request.query_params.get('name_contains')
        queryset=None

        print('got the queries in viewset company:{} ,category:{} ,product_name_contains{}'.format(company,category,product_name_contains))
        if company and category and product_name_contains:
            queryset=Product.objects.all().filter(brand_name__contains=company,product_category=category,name__contains=product_name_contains)
        elif company and category:
            queryset=Product.objects.all().filter(brand_name__contains=company,product_category=category)
        elif category and product_name_contains:
            queryset=Product.objects.all().filter(product_category=category,name__contains=product_name_contains)
        elif product_name_contains and company:
            queryset=Product.objects.all().filter(brand_name__contains=company,name__contains=product_name_contains)
        elif company:
            queryset=Product.objects.all().filter(brand_name__contains=company)
        elif category:
            queryset=Product.objects.all().filter(product_category=category)
        elif product_name_contains:
            queryset=Product.objects.all().filter(name__contains=product_name_contains)
        else:
            queryset=Product.objects.all()

        return queryset

class ProductDetailViewSet(viewsets.ModelViewSet):
    # queryset = Product.objects.all()
    serializer_class = ProductDetailsSerilizer
    def list(self,request,productId=None):
        if productId:
            print('getting some details about product id {}'.format(productId))
            try:
                productObject=Product.objects.get(id=productId)
                # see if we have a productDetail object for this
                productDetailsObjects=ProductDetail.objects.all().filter(product=productObject.id)
                if len(productDetailsObjects)==1:
                    print('returning the cache data')
                    serialized_data=ProductDetailsSerilizer(productObject,many=False)
                    return JsonResponse(serialized_data.data,safe=False)
                else:
                    print('scraping the data')
                    print('getting the product {}'.format(productObject.name))
                    json_spec_all,json_images,reviewsDict = scrapTheDetails(driver=productDetailsdriver,url=productObject.flipkart_link,callFromMain=False)
                    # print('got the spec len{} and images len{} and reviews: {}'.format(len(json_spec_all),len(json_images),len(reviewsDict)))
                    saveProductDetailsToDB(productObject,json_spec_all,json_images,reviewsDict)
                    # get the saved data and return it
                    new_product_detail_object=Product.objects.get(id=productId)
                    serialized_data=ProductDetailsSerilizer(new_product_detail_object,many=False)
                    return JsonResponse(serialized_data.data,safe=False)
            except Exception as e:
                print("got error {}".format(e))
                return Response('Error: '.format(e),status= 404)
        else:
            # FIXME pagination problem https://stackoverflow.com/questions/50878730/django-rest-framework-viewset-loses-pagination-searchfilter-and-orderingfilter
            return JsonResponse(ProductDetailsSerilizer(Product.objects.all(),many=True).data,safe=False)

class ProductFullSpecViewSet(viewsets.ModelViewSet):
    serializer_class = ProductFullSpecsSerializer
    def list(self,request,productId=None):
        if productId:
            print('searching full-spec for product id '+productId)
            all_specs_objects=ProductDetail.objects.all().filter(product=productId)
            serializer = self.get_serializer(all_specs_objects[0], many=False)
            return Response(serializer.data)
        else:
            print('getting all reviews')
            all_specs_objects=ProductDetail.objects.all()
            serializer = self.get_serializer(all_specs_objects, many=True)
            return Response(serializer.data)

class LatestMobilesViewSet(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    def list(self,request):
        allProducts=Product.objects.all().filter(product_category='mobiles')
        subset=allProducts[:8]
        serializer = self.get_serializer(subset, many=True)
        return Response(serializer.data)

class ecommerceBasedSearchViewSet(viewsets.ModelViewSet):
    serializer_class=ProductSerializer
    def get_queryset(self):
        ecommerce_site=self.request.query_params.get('site')
        category_name=self.request.query_params.get('category')
        sub_category=self.request.query_params.get('sub_category')
        print("site: {}, category: {}, brand: {}".format(ecommerce_site,category_name,sub_category))
        if ecommerce_site=='amazon':
            requiredQuerySet=Product.objects.all().filter(product_category=category_name,name__contains=sub_category,ecommerce_company=ecommerce_site).order_by('amazon_price')
        elif ecommerce_site=='flipkart':
            requiredQuerySet=Product.objects.all().filter(product_category=category_name,name__contains=sub_category,ecommerce_company=ecommerce_site).order_by('flipkart_price')
        return requiredQuerySet

