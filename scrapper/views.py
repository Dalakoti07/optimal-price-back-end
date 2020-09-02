from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
# Create your views here.
from .scrapFromFlipKart import getTheData
from .models import Product
from django.http import HttpResponse, JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# selenium and web scrapping stuff
import argparse
baseurl='https://www.flipkart.com/search?q='
import time
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
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
        driver=webdriver.Chrome('./driver')
        responseFromFunc=getTheData(driver,searchKey,False)
        # driver.close()
        if responseFromFunc:
            serialisedData=ProductSerializer(responseFromFunc,many=True)
            return JsonResponse(serialisedData.data,safe=False)
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
