# default image https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6
baseurl='https://www.flipkart.com/search?q='
import argparse
import time
from bs4 import BeautifulSoup
from requests import get
import sys
import csv
import json
import sys, os
# comment below line for when running from main 
# from .models import Product

def saveTheResultsToFile(fileName,productsDict):
    with open(fileName, 'w', newline='') as csvfile:
        if len(productsDict)==0:
            return
        csvWriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        print("len of product dict: "+str(len(productsDict)))
        for d in productsDict:
            # print("writing {}".format(d))
            each_product=productsDict[d]
            csvWriter.writerow( each_product[detail] for detail in each_product)

def extractTheDataFromEachProductCard(eachCardDiv,classNameAttributes,nested=False):
    localProductdict=None
    
    name=eachCardDiv.find('a' if nested else 'div', attrs={'class':classNameAttributes['name']})
    price=eachCardDiv.find('div' if nested else 'div', attrs={'class':classNameAttributes['price']})
    rating=eachCardDiv.find('div' if nested else 'div', attrs={'class':classNameAttributes['rating']})
    product_page=None
    if nested:
        product_page=eachCardDiv.findAll('a',attrs={'class':classNameAttributes['href_product']})
        if len(product_page)==1:
            product_page=product_page[0]['href']
        else:
            product_page='NA'
    else:
        product_page=eachCardDiv['href']
    product_page='https://www.flipkart.com'+product_page
    imageDiv=eachCardDiv.find('div',attrs={'class':classNameAttributes['image']})
    image_url='default.jpg'
    if imageDiv:
        allImages=imageDiv.findAll('img',src=True)
        for img in allImages:
            image_url=img['src']
    # print("name: {}, price:{} ".format(name.text,price.text))
    localProductdict= {
        "name":name.text.split('(')[0] if name else "NA",
        "price":price.text if price else "NA",
        "rating":rating.text if rating else "NA",
        "image_url":image_url if image_url else "NA",
        "product_page":product_page if product_page else "NA"
    }
    return localProductdict
    

#function used for scrapping in getthedata working for only mobiles
def getTheData(driver,keyword='mobile',callFromMain=True):
    listOfProducts=[]
    
    url = baseurl+keyword
    driver.get(url)
    time.sleep(3)
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # for writing in csv
    productsDict={}
    colInRow=False
    typeOfCardInARow=None
    with open('./ecommerceClasses.json') as f:
        classNameAttributes = json.load(f)
    if keyword in ['mobile','laptop']:
        # webpages with box in each row
        typeOfCardInARow='a'
        classNameAttributes=classNameAttributes["flipkart"][keyword]
    else :
        # webpages with m boxes in each row
        typeOfCardInARow='div'
        colInRow=True
        print('keyword is {}'.format(keyword))
        classNameAttributes=classNameAttributes["flipkart"][keyword]
        # return listOfProducts
    i=0
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
                    productDict=extractTheDataFromEachProductCard(eachCardDiv=eachCol,classNameAttributes=classNameAttributes,nested=True)
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
                pass
                # product=Product(name=name.text,rating=rating.text,image_url=image_url,price=price.text)
                # product.save()
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

    print('length of data scrapped: '+str(len(listOfProducts)))
    return listOfProducts
    
    # print('one url '+listOfProducts[0].image_url+listOfProducts[4].image_url)
    

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
    
    getTheData(driver,args.item)
else:
    print("Executed when imported")