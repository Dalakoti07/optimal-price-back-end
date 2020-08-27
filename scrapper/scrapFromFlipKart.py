import argparse
baseurl='https://www.flipkart.com/search?q='
import time
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
driver=webdriver.Chrome('./driver')
import sys 

# default image https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6
# see coding standards and insight from https://github.com/c17hawke/flask-based-wordcloud-generator/blob/master/app.py
class Product():
    def __init__(self,name,rating,image_url,price):
        self.name=name
        self.rating=rating
        self.image_url=image_url
        self.price=price

    def __str__(self):
        return "{} has imageUrl: {}".format(self.name,self.image_url)
    
    def __repr__(self):
        return "{} has Price: {}".format(self.name,self.price)

# class used for scrapping in getthedata working for only mobiles
def getTheData(keyword='mobiles'):
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
        # img src are put by js script, thus src not available in src code, thus requests fail and u have to use selenium

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
        
        listOfProducts.append(Product(name.text,rating.text,image_url,price.text))

    print(len(listOfProducts))
    # print('one url '+listOfProducts[0].image_url+listOfProducts[4].image_url)

parser = argparse.ArgumentParser()
parser.add_argument("--item", help="enter the item name you want to search on flipkart",type=str)
args = parser.parse_args()

if __name__ == "__main__":
    print("main function directly called and its is running and keyword searched :"+args.item)
    getTheData(args.item)
else:
    print("Executed when imported")