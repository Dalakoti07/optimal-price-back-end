# default image https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6
baseurl='https://www.flipkart.com/search?q={}&page={}'
import argparse
import time
from bs4 import BeautifulSoup
from requests import get
import sys
import csv
import json
import sys, os
# comment below line for when running from main 

def extractTheDataFromEachProductCard(eachCardDiv,classNameAttributes,nested=False,takeCompany=False):
    localProductdict=None
    companyName=None
    if takeCompany:
        companyName=eachCardDiv.find('div',attrs={'class':classNameAttributes['company_name']})
    name=eachCardDiv.find('a' if nested else 'div', attrs={'class':classNameAttributes['name']})
    price=eachCardDiv.find('div' if nested else 'div', attrs={'class':classNameAttributes['price']})
    rating=eachCardDiv.find('div' if nested else 'div', attrs={'class':classNameAttributes['rating']})
    product_page=None
    if nested:
        product_page=eachCardDiv.findAll('a',attrs={'class':classNameAttributes['href_product']})
        if len(product_page)==1:
            product_page=product_page[0]['href']
        else:
            product_page=None
    else:
        product_page=eachCardDiv['href']
    if product_page:
        product_page='https://www.flipkart.com'+product_page
    imageDiv=eachCardDiv.find('div',attrs={'class':classNameAttributes['image']})
    image_url='default.jpg'
    if imageDiv:
        allImages=imageDiv.findAll('img',src=True)
        for img in allImages:
            image_url=img['src']
    # print("name: {}, price:{} ".format(name.text,price.text))
    localProductdict= {
        "name":(companyName.text if (takeCompany and companyName) else '')+' ' + (name.text if name else "NA") ,
        "price":price.text if price else "None",
        "rating":rating.text if rating else "None",
        "image_url":image_url if image_url else "None",
        "product_page":product_page if product_page else "None"
    }
    return localProductdict
    

#function used for scrapping in getthedata working for only mobiles
def scrapAPage(driver,keyword='mobile',callFromMain=True,page_number=0):
    listOfProducts=[]
    
    url = baseurl.format(keyword,page_number)
    print("fetching the url..........{}".format(url))
    driver.get(url)
    time.sleep(1)
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # for writing in csv
    productsDict={}
    colInRow=False
    typeOfCardInARow=None
    getCompany=False
    if callFromMain:
        with open('./ecommerceClassesConfig.json') as f:
            classNameAttributes = json.load(f)
    else:
        with open('./scrapper/ecommerceClassesConfig.json') as f:
            classNameAttributes = json.load(f)

    if ('mobile' in keyword) or ('laptop' in keyword):
        # webpages with box in each row
        typeOfCardInARow='a'
        classNameAttributes=classNameAttributes["flipkart"]['mobile']
    elif ('books' in keyword) or ('electronics' in keyword):
        # webpages with m boxes in each row
        typeOfCardInARow='div'
        colInRow=True
        print('keyword is {}'.format(keyword))
        classNameAttributes=classNameAttributes["flipkart"]['books']
    elif ('shirts' in keyword) or ('jacket' in keyword) or ('shoes' in keyword) or ('jeans' in keyword):
        getCompany=True
        typeOfCardInARow='div'
        colInRow=True
        print('keyword is {}'.format(keyword))
        classNameAttributes=classNameAttributes["flipkart"]['fashion']
    else:
        print('not handled that')
        driver.close()
        return listOfProducts
    i=0
    # assuming that one product in 1 row => 1 'a' in each row, otherwise m product in each row means div as one row and m 'a' in it
    for eachRow in html_soup.findAll(typeOfCardInARow,href=False if colInRow else True, attrs={'class':classNameAttributes['card']}):
        if not colInRow:
                i+=1
        print("item number {}".format(i),end='\t')
        productDict=None
        # href in card class and href attribute
        try:
            if colInRow:
                # many product in one row
                print("many product in one row")
                for eachCol in eachRow.findAll('div',attrs={'class':classNameAttributes['nested_card']}):
                    productDict=None
                    i+=1
                    productDict=extractTheDataFromEachProductCard(eachCardDiv=eachCol,classNameAttributes=classNameAttributes,nested=True,takeCompany=getCompany)
                    if not productDict:
                        continue
                    else:
                        print("Name: {} and imageUrl: {}".format(productDict['name'],productDict['image_url']),end=' ')
                        productsDict["product-{}".format(i)]=productDict
            else:
                # single product in single row
                # print("single product in single row")
                productDict=extractTheDataFromEachProductCard(eachCardDiv=eachRow,classNameAttributes=classNameAttributes)
            if not callFromMain:
                print("django running saving {}-product.....".format(i))
                from .ScrappedItem import ScrappedItem
                if productDict:
                    product=ScrappedItem(name=productDict['name'],rating=productDict['rating'],
                            image_url=productDict['image_url'],price=productDict['price'],href=productDict['product_page'])
                    listOfProducts.append(product)
            else:
                if not colInRow:
                    print("Name: {} and imageUrl: {}".format(productDict['name'],productDict['image_url']),end=' ')
                    productsDict["product-{}".format(i)]=productDict
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("exception at item-{},{},{},{},message:{}".format(i,exc_type, fname, exc_tb.tb_lineno,e))

    if callFromMain:
        from ScrapperUtils import saveTheResultsToFile
        saveTheResultsToFile('csvs/flipkart-{}.csv'.format(keyword),productsDict)

    print('length of data scrapped: '+str(len(listOfProducts)))
    return listOfProducts
    
    # print('one url '+listOfProducts[0].image_url+listOfProducts[4].image_url)

def scrapMultiplePages(driver,keyword,pageCount):
    productsFromAllPages=[]
    for p in range(0,pageCount):
        productsFromAllPages = productsFromAllPages + scrapAPage(driver=driver,keyword=keyword,callFromMain=False,page_number=p)
    return productsFromAllPages

if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    parser = argparse.ArgumentParser()
    parser.add_argument("--item", help="enter the item name you want to search on flipkart",type=str)
    args = parser.parse_args()

    print("main function directly called and its is running and keyword searched :"+args.item)
    service = Service('./driver')
    service.start()
    driver=webdriver.Remote(service.service_url) 
    
    scrapAPage(driver,args.item)
else:
    print("Executed when imported")