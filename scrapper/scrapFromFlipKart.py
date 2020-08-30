# default image https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6
# see coding standards and insight from https://github.com/c17hawke/flask-based-wordcloud-generator/blob/master/app.py
baseurl='https://www.flipkart.com/search?q='
import argparse
import time
from bs4 import BeautifulSoup
from requests import get
import sys 
from .models import Product

#function used for scrapping in getthedata working for only mobiles
def getTheData(driver,keyword='mobiles'):
    listOfProducts=[]
    
    url = baseurl+keyword
    driver.get(url)
    time.sleep(3)
    html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    i=0
    for a in html_soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
        i+=1
        name=a.find('div', attrs={'class':'_3wU53n'})
        price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
        rating=a.find('div', attrs={'class':'hGSR34'})
        # https://stackoverflow.com/questions/57287726/not-able-to-scrap-the-images-from-flipkart-com-website-the-src-attribute-is-comi
        # img src put by js script, thus src not available in src code, thus requests fail and u have to use selenium

        # print("name: {} and price: {}".format(name.text,price.text))
        if i==5:
            print(a)
        imageDiv=a.find('img',attrs={'class':'_1Nyybr _30XEf0'})
        image_url=None
        if imageDiv ==None:
            image_url='placeholder.url'
        else:
            image_url=imageDiv['src']
        print(image_url)
        product=Product(name=name.text,rating=rating.text,image_url=image_url,price=price.text)
        product.save()
        listOfProducts.append(product)

    print('length of data scrapped: '+str(len(listOfProducts)))
    return listOfProducts
    # print('one url '+listOfProducts[0].image_url+listOfProducts[4].image_url)

if __name__ == "__main__":
    from selenium import webdriver
    driver=webdriver.Chrome('./driver')

    parser = argparse.ArgumentParser()
    parser.add_argument("--item", help="enter the item name you want to search on flipkart",type=str)
    args = parser.parse_args()

    print("main function directly called and its is running and keyword searched :"+args.item)
    getTheData(driver,args.item)
else:
    print("Executed when imported")