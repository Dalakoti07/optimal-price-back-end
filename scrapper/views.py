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
from .ScrapperUtils import serialiseTheScrappedPagesIntoCSV,mergeList,saveToDB,deserialiseTheListFromCSV,pseudoMergeIt
from .amazonScrapper import scrapAPage as amazonScrapAPage,scrapMultiplePages as amazonScrapMultiplePage

# selenium and web scrapping stuff
import argparse
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
def returnJsonResponseFromProductList(productList,totalTime):
    data=[]
    for p in productList:
        data.append({
            "name":p.name,
            "rating":p.rating,
            "image_url":p.image_url,
            "price":p.price,
            "brand_name":p.brand_name,
            "amazon_link":p.amazon_link,
            "flipkart_link":p.flipkart_link,
            "product_category":p.product_category
        })
    response={
        "time-taken":str(totalTime),
        "length":len(data),
        "data":data
    }
    return response

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
        amazonItems,category_type=amazonScrapMultiplePage(driver,searchKey,pagesLimit)
        print("{} items scrapped from amazon".format(len(amazonItems)))
        serialiseTheScrappedPagesIntoCSV(amazonItems,"./scrapper/csvs/amazon-django-{}_pages-{}.csv".format(pagesLimit,searchKey))

        # driver.close()
        elapsed_time = time.perf_counter() - start_time
        if category_type=='fashion':
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
            saveToDB(merged_list)
            return JsonResponse( returnJsonResponseFromProductList( merged_list,totalTime=elapsed_time),safe=False)
        else:
            return HttpResponse('Server Error')
        

        # unit testing for db
        # saveToDB(mergeList(deserialiseTheListFromCSV("./scrapper/csvs/flipkart-django-5_pages-samsung phones.csv"),deserialiseTheListFromCSV("./scrapper/csvs/amazon-django-5_pages-samsung phones.csv"),categoryType='mobiles'))
        # return JsonResponse('it should be done',safe=False)

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

def searchByCategory(request):
    if request.method=='GET':
        category_name=str(request.GET['category'])
        print('category key: '+category_name)
        filtered_products=Product.objects.filter(product_category=category_name)
        serialized_data=ProductSerializer(filtered_products,many=True)
        return JsonResponse(serialized_data.data,safe=False)
    else:
        return HttpResponseBadRequest('Method Not allowed')

'''
    data = JSONParser().parse(request)
    print('data search_key:{}'.format(data['search']))
    return HttpResponse('returning ')
'''
