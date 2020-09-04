if __name__ == "__main__":
    from ScrappedItem import ScrappedItem
else:
    from .ScrappedItem import ScrappedItem

import csv
from difflib import SequenceMatcher
def cleanDataAndGetTokens(currentString):
    currentString=currentString.replace('(','')
    currentString=currentString.replace(')','')
    currentString=currentString.replace(',','')
    wordsToken=currentString.split(' ')
    return wordsToken

def tokensEqual(tokens1,tokens2):
    # make custom
    pass

def validateData():
    pass

def createNewItem(fi,ai,categorytype='simple'):
    # priority wise attributes
    # name - flip, rating -flip, imageurl flip else amazon
    # price -amazon, 
    name=fi.name if fi.name else ai.name
    name=name.strip()
    rating=fi.rating if fi.rating else ai.rating.split('out')[0]
    image_url=fi.image_url if not '.svg' in fi.image_url else ai.image_url

    price=int(ai.price.replace(',','').replace('₹','')) if ai.price else (int(fi.price.replace('₹','').replace(',','')) if fi.price else None)

    item= ScrappedItem(name=name,rating=rating,image_url= image_url
        ,price= price,href=None)
    # adding extra attributes [item's brand_name, amazon_link,flipkart_link,product_category]
    item.brand_name=item.name.split(' ')[0]
    item.amazon_link=ai.href
    item.flipkart_link=fi.href
    item.product_category=categorytype
    # validate data before saving it in db
    return item

def mergeList(amazonList,flipkartList):
    # merge the list
    mergedItems=[]
    for fi in flipkartList:
        nameToBeSearched=cleanDataAndGetTokens(fi.name.strip())
        # remove useless chars
        for ai in amazonList:
            currentName=cleanDataAndGetTokens(ai.name.strip())
            if SequenceMatcher(None, nameToBeSearched, currentName).ratio() >=0.7:
                # create mergedObject
                new_item=createNewItem(fi,ai)

                mergedItems.append(new_item)
                # break because not more than one match for each item
                break
    return mergedItems
    
def saveTheResultsToFile(fileName,productsDict):
    with open(fileName, 'w', newline='') as csvfile:
        if len(productsDict)==0:
            return
        csvWriter = csv.writer(csvfile, delimiter=';',quoting=csv.QUOTE_MINIMAL)
        print("len of product dict: "+str(len(productsDict)))
        for d in productsDict:
            # print("writing {}".format(d))
            each_product=productsDict[d]
            csvWriter.writerow( each_product[detail] for detail in each_product)

def saveTheMergeListIntoCSV(productList,fileName):
    with open(fileName, 'w', newline='') as csvfile:
        if len(productList)==0:
            return
        csvWriter = csv.writer(csvfile, delimiter=';',quoting=csv.QUOTE_MINIMAL)
        print("len of product list which is being serialised is : "+str(len(productList)))
        for d in productList:
            # print("writing {}".format(d))
            name = d.name
            rating = d.rating
            image_url=d.image_url
            price=d.price
            amazon_link=d.amazon_link
            flipkart_link=d.flipkart_link
            brand_name=d.brand_name
            csvWriter.writerow( detail for detail in [name,brand_name,rating,image_url,price,amazon_link,flipkart_link])

def serialiseTheScrappedPagesIntoCSV(productList,fileName):
    with open(fileName, 'w', newline='') as csvfile:
        if len(productList)==0:
            return
        csvWriter = csv.writer(csvfile, delimiter=';',quoting=csv.QUOTE_MINIMAL)
        print("len of product list which is being serialised is : "+str(len(productList)))
        for d in productList:
            # print("writing {}".format(d))
            name = d.name
            rating = d.rating
            image_url=d.image_url
            price=d.price
            href=d.href
            csvWriter.writerow( detail for detail in [name,rating,image_url,price,href])

def deserialiseTheListFromCSV(fileName):
    itemList=[]
    with open(fileName, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            product =ScrappedItem(name= row[0],rating= row[1],image_url= row[2],price= row[3],href=row[4])
            itemList.append(product)
    return itemList


mList= mergeList(deserialiseTheListFromCSV("./csvs/flipkart-django-10_pages-mobile.csv"),deserialiseTheListFromCSV("./csvs/amazon-django-10_pages-mobile.csv"))
print("len of intersection item: {}".format(len(mList)))

saveTheMergeListIntoCSV(mList,"./csvs/merged-mobile-amaon-flipkart.csv")