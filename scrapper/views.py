from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer

# Create your views here.
from .models import Product
from django.http import HttpResponse, JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# utils function import
from .flipkartScrapper import scrapAPage as flipkartScrapAPage,scrapMultiplePages as flipkartScrapMultiplePage
from .ScrapperUtils import serialiseTheScrappedPagesIntoCSV
from .amazonScrapper import scrapAPage as amazonScrapAPage,scrapMultiplePages as amazonScrapMultiplePage

# selenium and web scrapping stuff
import argparse
baseurl='https://www.flipkart.com/search?q='
import time
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
# use selenium service to avoid too much rersource usage
import sys 


'''
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
'''

def search_by_scrap(request):
    if request.method=='GET':
        searchKey=str(request.GET['search'])
        print('scrapping : '+searchKey)
        
        # start service of selenium and prepare the driver
        service = Service('./driver')
        service.start()
        driver=webdriver.Remote(service.service_url)

        pagesLimit=10
        # scrap the data from flipkart 
        flipkartItems=flipkartScrapMultiplePage(driver,searchKey,pagesLimit)
        print("{} items scrapped from flipkart".format(len(flipkartItems)))
        serialiseTheScrappedPagesIntoCSV(flipkartItems,"./scrapper/csvs/flipkart-django-{}-pages-{}.csv".format(5,searchKey))
        
        # launch a new tab,its optional

        # scrap the data from amazon
        amazonItems=amazonScrapMultiplePage(driver,searchKey,pagesLimit)
        print("{} items scrapped from amzon".format(len(amazonItems)))
        serialiseTheScrappedPagesIntoCSV(amazonItems,"./scrapper/csvs/amazon-django-{}-pages-{}.csv".format(5,searchKey))

        # driver.close()
        
        if amazonItems and flipkartItems:
            # serialisedData=ProductSerializer(responseFromFunc,many=True)
            return JsonResponse('success: flipkartItem: {} and amazonItems: {}'.format(len(flipkartItems),len(amazonItems)),safe=False)
        else:
            return HttpResponse('Server Error')

def search_in_db(request):
    if request.method=='GET':
        searchWord=str(request.GET['search'])
        print('search key: '+str(request.GET['search']))
        filtered_products=Product.objects.filter(name__contains=searchWord)
        serialized_data=ProductSerializer(filtered_products,many=True)
        return JsonResponse(serialized_data.data,safe=False)
    else:
        return HttpResponseBadRequest('Method Not allowed')

def viewAllProducts(request):
    if request.method=='GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        HttpResponseBadRequest('Method Not allowed ')

'''
    data = JSONParser().parse(request)
    print('data search_key:{}'.format(data['search']))
    return HttpResponse('returning ')
'''
