# default image https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6
baseurl='https://www.amazon.in/s?k='
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
        "name":(companyName.text if (takeCompany and companyName) else '')+' ' + (name.text.split('(')[0] if name else "NA") ,
        "price":price.text if price else "None",
        "rating":rating.text if rating else "None",
        "image_url":image_url if image_url else "None",
        "product_page":product_page if product_page else "None"
    }
    return localProductdict

#function used for scrapping in getthedata working for only mobiles
def getTheData(driver,keyword='mobile',callFromMain=True):
    listOfProducts=[]
    
    url = baseurl+keyword
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

    with open('./ecommerceClassesConfig.json') as f:
        classNameAttributes = json.load(f)
    if (keyword in ['mobile','laptop']) or ('books' in keyword):
        # webpages with box in each row
        typeOfCardInARow='div'
        classNameAttributes=classNameAttributes["amazon"]['mobile']
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
            pass
            # product=Product(name=name.text,rating=rating.text,image_url=image_url,price=price.text)
            # product.save()
            listOfProducts.append(product)
        print("\n")

    if callFromMain:
        saveTheResultsToFile('csvs/amazon-{}.csv'.format(keyword),productsDict)

    print('length of data scrapped: '+str(len(listOfProducts)))
    if callFromMain:
        driver.close()
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