# default image https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6
baseurl='https://www.amazon.in/s?k={}&page={}'
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
    name=eachCardDiv.find('span', attrs={'class':classNameAttributes['name']})
    price=eachCardDiv.find('span', attrs={'class':classNameAttributes['price']})
    rating=eachCardDiv.find('a', attrs={'class':classNameAttributes['rating']})
    rating =rating.i.span if rating else None
    product_page=eachCardDiv.findAll('a',attrs={'class':classNameAttributes['href_product']})
    if len(product_page)==1:
        product_page=product_page[0]['href']
    else:
        product_page=None
    
    product_page=('https://www.amazon.in'+product_page) if product_page else "None"
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
    driver.get(url)
    time.sleep(3)
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # save file for saving data
    # with open("/htmls/amazon-{}.html".format(keyword), 'w', newline='') as htmlFile:
        # htmlFile.write(driver.page_source)
    
    # for writing in csv
    productsDict={}
    colInRow=False
    typeOfCardInARow=None
    getCompany=False
    product_category=None

    if callFromMain:
        with open('./ecommerceClassesConfig.json') as f:
            classNameAttributes = json.load(f)
    else:
        with open('./scrapper/ecommerceClassesConfig.json') as f:
            classNameAttributes = json.load(f)
    if ('mobiles' in keyword) or ('laptops' in keyword) or ('books' in keyword) or ('phones' in keyword):
        # webpages with box in each row
        typeOfCardInARow='div'
        classNameAttributes=classNameAttributes["amazon"]['mobiles']
        product_category = 'mobiles' if (('mobiles' in keyword) or ('phones' in keyword)) else ('computer' if ('laptops' in keyword) else 'books')
    elif keyword in ['electronics']:
        # webpages with m boxes in each row
        typeOfCardInARow='div'
        colInRow=True
        print('keyword is {}'.format(keyword))
        classNameAttributes=classNameAttributes["amazon"]['multiple']
    elif ('shirts' in keyword) or ('jacket' in keyword) or ('shoes' in keyword) or ('jeans' in keyword):
        getCompany=True
        typeOfCardInARow='div'
        colInRow=True
        print('keyword is {}'.format(keyword))
        classNameAttributes=classNameAttributes["amazon"]['multiple']
        product_category='fashion'
    else:
        print('not handled that')
        driver.close()
        return listOfProducts

    i=0
    # flipkart has a card in a row bounded with a ,but in amazon they have no div/a wrapper in each row
    # small or medium card is always div in flipkart
    for eachItem in html_soup.findAll('div', attrs={'class':classNameAttributes['card']}):
        i+=1

        print("item number {}".format(i),end='\t')
        productDict=None
        # href in _31qSD5 class and href attribute
        try:
            productDict=extractTheDataFromEachProductCard(eachCardDiv=eachItem,classNameAttributes=classNameAttributes,takeCompany=getCompany)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("exception at item-{},{},{},{},message:{}".format(i,exc_type, fname, exc_tb.tb_lineno,e))
            continue
        
        if callFromMain:
            print("Name: {} and imageUrl: {}".format(productDict['name'],productDict['image_url']),end=' ')
            productsDict["product-{}".format(i)]=productDict
        else:
            print("django running saving {}-product.....".format(i))
            from .ScrappedItem import ScrappedItem
            if productDict:
                product=ScrappedItem(name=productDict['name'],rating=productDict['rating'],
                        image_url=productDict['image_url'],price=productDict['price'],href=productDict['product_page'])
                listOfProducts.append(product)
        print("\n")

    if callFromMain:
        from ScrapperUtils import saveTheResultsToFile
        saveTheResultsToFile('csvs/amazon-{}.csv'.format(keyword),productsDict)

    print('length of data scrapped: '+str(len(listOfProducts)))
    if callFromMain:
        driver.close()
    return (listOfProducts,product_category)

def scrapMultiplePages(driver,keyword,pageCount):
    productsFromAllPages=[]
    for p in range(0,pageCount):
        received_items,product_category = scrapAPage(driver=driver,keyword=keyword,callFromMain=False,page_number=p+1)
        productsFromAllPages= list(received_items) + productsFromAllPages
    return (productsFromAllPages,product_category)

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