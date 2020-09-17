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
        "price":price.text if price else None,
        "rating":rating.text if rating else None,
        "image_url":image_url if image_url else None,
        "product_page":product_page if product_page else None
    }
    return localProductdict

def readConfigFile(callFromMain):
    JsonFile=None
    if callFromMain:
        with open('./ecommerceClassesConfig.json') as f:
            JsonFile = json.load(f)
    else:
        with open('./scrapper/ecommerceClassesConfig.json') as f:
            JsonFile = json.load(f)
    return JsonFile

#function used for scrapping in getthedata working for only mobiles
def scrapAPage(driver,keyword='mobile',callFromMain=True,page_number=0):
    listOfProducts=[]
    
    url = baseurl.format(keyword,page_number)
    print("fetching the url..........{}".format(url))
    try :
        driver.get(url)
    except Exception as e:
        print("got an dirver exception return")
        return listOfProducts    
    time.sleep(1)
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # for writing in csv
    productsDict={}
    colInRow=False
    typeOfCardInARow=None
    getCompany=False
    product_category=None
    classNameAttributes=readConfigFile(callFromMain)

    if ('mobile' in keyword) or ('laptop' in keyword) or ('phone' in keyword) or ('refrigerator' in keyword) or ('television' in keyword) or ('camera' in keyword) :
        # webpages with box in each row
        typeOfCardInARow='a'
        classNameAttributes=classNameAttributes["flipkart"]['mobiles']
        product_category = 'mobiles' if (('mobiles' in keyword) or ('phones' in keyword)) else 'computer'
    elif ('books' in keyword):
        # webpages with m boxes in each row
        typeOfCardInARow='div'
        colInRow=True
        print('keyword is {}'.format(keyword))
        classNameAttributes=classNameAttributes["flipkart"]['books']
        product_category='books' if ('book' in keyword) else 'electronics'
    elif ('shirt' in keyword) or ('jacket' in keyword) or ('shoe' in keyword) or ('jean' in keyword):
        getCompany=True
        typeOfCardInARow='div'
        colInRow=True
        print('keyword is {}'.format(keyword))
        classNameAttributes=classNameAttributes["flipkart"]['fashion']
        product_category='fashion'
    else:
        print('not handled that')
        return listOfProducts
    i=0
    if not callFromMain:
        from .ScrappedItem import ScrappedItem
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
                        # print("Name: {} and imageUrl: {}".format(productDict['name'],productDict['image_url']),end=' ')
                        productsDict["product-{}".format(i)]=productDict
                        product=ScrappedItem(name=productDict['name'],rating=productDict['rating'],
                            image_url=productDict['image_url'],price=productDict['price'],href=productDict['product_page'])
                        listOfProducts.append(product)
            else:
                # single product in single row
                # print("single product in single row")
                productDict=extractTheDataFromEachProductCard(eachCardDiv=eachRow,classNameAttributes=classNameAttributes)
            if not callFromMain:
                print("django running saving {}-product.....".format(i))
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
        saveTheResultsToFile('csvs/flipkart-{}.csv'.format(keyword),productsDict)

    print('length of data scrapped from 1 page: '+str(len(listOfProducts)))
    return (listOfProducts,product_category)
    
    # print('one url '+listOfProducts[0].image_url+listOfProducts[4].image_url)

def scrapMultiplePages(driver,keyword,pageCount):
    productsFromAllPages=[]
    for p in range(0,pageCount):
        received_items,product_category = scrapAPage(driver=driver,keyword=keyword,callFromMain=False,page_number=p+1)
        productsFromAllPages= list(received_items) + productsFromAllPages 
    #praoduct_category returned from here wont affect anything 
    return productsFromAllPages,product_category

def scrapDeals(driver,callFromMain=False):
    base_url_deals='https://www.flipkart.com'
    driver.get(base_url_deals)
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    jsonFile=readConfigFile(callFromMain)
    classNameAttributes=jsonFile['flipkart']['deals']
    results={}
    i=1
    for eachCard in html_soup.find_all('a',href=True,attrs={'class':classNameAttributes['card']}):
        href_link=base_url_deals+ eachCard['href']
        imageDivs=eachCard.findAll('img',{"src":True})
        image_url=None
        if len(imageDivs)>=1 :
            image_url=imageDivs[0]['src']
        results["deal-{}".format(i)]={
            "image_url":image_url,
            "href_link":href_link
        }
        i=i+1
    # print(results)
    return results

if __name__ == "__main__":
    from ScrapperUtils import saveTheResultsToFile

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--item", help="enter the item name you want to search on flipkart",type=str)
    args = parser.parse_args()

    print("main function directly called and its is running and keyword searched :"+args.item)
    service = Service('./driver')
    service.start()
    driver=webdriver.Remote(service.service_url) 
    if args.item=='deals':
        scrapDeals(driver,callFromMain= True)
    else:
        scrapAPage(driver,args.item)
    # driver.close()
else:
    print("Executed when imported")

