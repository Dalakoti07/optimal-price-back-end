baseurl='https://www.flipkart.com/search?q='
from bs4 import BeautifulSoup
from requests import get

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

def getTheData():
    keyword='asus+mobile'
    listOfProducts=[]
    
    url = baseurl+keyword
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    for a in html_soup.findAll('a',href=True, attrs={'class':'_31qSD5'}):
        name=a.find('div', attrs={'class':'_3wU53n'})
        price=a.find('div', attrs={'class':'_1vC4OE _2rQ-NK'})
        rating=a.find('div', attrs={'class':'hGSR34'})
        # _3btv9x has image tag and that class has _1nyybr name
        # imageDiv=a.find('div',attrs={'class':'_3btv9x'})
        image_url=''
        # if imageDiv.img:
            # image_url=imageDiv.img['src']
        listOfProducts.append(Product(name.text,rating.text,image_url,price.text))

    print(len(listOfProducts))
    # print('one url '+listOfProducts[0].image_url+listOfProducts[4].image_url)

if __name__ == "__main__":
    print("main is running ")
    getTheData()
else:
    print("Executed when imported")