# default image https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6
baseurl='https://www.flipkart.com/search?q='
import argparse
import time
from bs4 import BeautifulSoup
from requests import get
import sys
import csv
import json
# comment below line for when running from main 
# from .models import Product

#function used for scrapping in getthedata working for only mobiles
def getTheData(driver,keyword='mobile',callFromMain=True):
    listOfProducts=[]
    
    url = baseurl+keyword
    driver.get(url)
    time.sleep(3)
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # for writing in csv
    productsDict={}
    with open('./ecommerceClasses.json') as f:
        classNameAttributes = json.load(f)
    if keyword in ['mobile','laptop']:
        classNameAttributes=classNameAttributes["flipkart"][keyword]
    else :
        print('Not coded for that')
        return listOfProducts
    i=0
    for a in html_soup.findAll('a',href=True, attrs={'class':classNameAttributes['card']}):
        i+=1

        print("item number {}".format(i),end='\t')
        # href in card class and href attribute
        try:
            name=a.find('div', attrs={'class':classNameAttributes['name']})
            price=a.find('div', attrs={'class':classNameAttributes['price']})
            rating=a.find('div', attrs={'class':classNameAttributes['rating']})
            product_page=a['href']
            product_page='https://www.flipkart.com'+product_page

            imageDiv=a.find('div',attrs={'class':classNameAttributes['image']})
            image_url='default.jpg'
            if imageDiv:
                allImages=imageDiv.findAll('img',src=True)
                for img in allImages:
                    image_url=img['src']
            # print(image_url,end='')
            if not callFromMain:
                pass
                # product=Product(name=name.text,rating=rating.text,image_url=image_url,price=price.text)
                # product.save()
                listOfProducts.append(product)
            else:
                print("Name: {} and imageUrl: {}".format(name.text.split('(')[0],image_url),end=' ')
                print("price: {} ".format(price.text))
                print("\n")
                
                productsDict["product-{}".format(i)]={
                    "name":name.text.split('(')[0],
                    "price":price.text,
                    "rating":rating.text,
                    "image_url":image_url,
                    "product_page":product_page
                }
        except:
            pass

    if callFromMain:
        with open('csvs/flipkart-{}.csv'.format(keyword), 'w', newline='') as csvfile:
            if len(productsDict)==0:
                return
            csvWriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
            print("len of product dict: "+str(len(productsDict)))
            for d in productsDict:
                # print("writing {}".format(d))
                each_product=productsDict[d]
                csvWriter.writerow( each_product[detail] for detail in each_product)

    print('length of data scrapped: '+str(len(listOfProducts)))
    return listOfProducts
    
    # print('one url '+listOfProducts[0].image_url+listOfProducts[4].image_url)
    

if __name__ == "__main__":
    from selenium import webdriver
    parser = argparse.ArgumentParser()
    parser.add_argument("--item", help="enter the item name you want to search on flipkart",type=str)
    args = parser.parse_args()

    print("main function directly called and its is running and keyword searched :"+args.item)
    driver=webdriver.Chrome('./driver')    
    getTheData(driver,args.item)
else:
    print("Executed when imported")