if __name__ == "__main__":
    from ScrappedItem import ScrappedItem
else:
    # call from django,
    # but it can be call from flipkart or amazon scrapper
    # comment it when not using django
    from .ScrappedItem import ScrappedItem
    from .models import Product
    pass

import csv
from difflib import SequenceMatcher
def cleanTheName(currentString):
    currentString=currentString.replace('(','')
    currentString=currentString.replace(')','')
    currentString=currentString.replace(',','')
    return currentString

def tokensEqual(tokens1,tokens2):
    # make custom
    # ToDo
    pass

def validateData():
    pass

def createNewItem(fi,ai,categorytype='simple'):
    # TODO make an attribute for amazon price and flipkart price
    # priority wise attributes
    # name - flip, rating -flip, imageurl flip else amazon
    # price -amazon, 
    name=fi.name if fi.name else ai.name
    name=name.strip()
    rating=fi.rating if fi.rating else ai.rating.split('out')[0]
    image_url=fi.image_url if not '.svg' in fi.image_url else ai.image_url
    price=None
    try:
        if fi.price:
            price=int(fi.price.replace('₹','').replace(',',''))
        elif ai.price:
            price=int(ai.price.replace(',','').replace('₹',''))
    except Exception as e:
        print("Error in processing price ")
        print(e)

    item= ScrappedItem(name=name,rating=rating,image_url= image_url
        ,price= price,href=None)
    # adding extra attributes [item's brand_name, amazon_link,flipkart_link,product_category]
    item.brand_name=item.name.split(' ')[0]
    item.amazon_link=ai.href
    item.flipkart_link=fi.href
    item.product_category=categorytype
    # validate data before saving it in db
    return item

def pseudoMergeIt(itemList,ecommerce_site,categoryType):
    print('pseudo merging it ')
    finalizeItems=[]
    for item in itemList:
        newItem= ScrappedItem(name=item.name,rating=item.rating,image_url=item.image_url,price=item.price,href=None)
        newItem.brand_name=newItem.name.split(' ')[0]
        if ecommerce_site=='amazon':
            newItem.amazon_link=item.href
            newItem.flipkart_link=None
            newItem.ecommerce_company='amazon'
        else:
            newItem.flipkart_link=item.href
            newItem.amazon_link=None
            newItem.ecommerce_company='flipkart'
        newItem.product_category=categoryType
        finalizeItems.append(newItem)
    return finalizeItems

def mergeList(amazonList,flipkartList,categoryType):
    # merge the list
    mergedItems=[]
    for fi in flipkartList:
        nameToBeSearched=cleanTheName(fi.name.strip())
        nameToBeSearched=nameToBeSearched[:50]
        # remove useless chars
        idx=0
        for ai in amazonList:
            currentName=cleanTheName(ai.name.strip())
            if SequenceMatcher(None, nameToBeSearched, currentName).ratio() >=0.7:
                # create mergedObject
                new_item=createNewItem(fi,ai,categorytype=categoryType)
                # remove ai from amazon-list so that it cannot be clubbed with anyone
                del amazonList[idx]
                mergedItems.append(new_item)
                # break because not more than one match for each item
                break
            else:
                idx+=1
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


def saveToDB(merged_list,save=True):
    i=0
    for m in merged_list:
        if m.name==None or m.price==None:
            continue
        if save:
            try:
                ecommerce_company_val='both'
                if hasattr(m, 'ecommerce_company'):
                    ecommerce_company_val=m.ecommerce_company
                product =Product(name=m.name,rating=m.rating,image_url=m.image_url,price=m.price,brand_name=m.brand_name,product_category=m.product_category,ecommerce_company=ecommerce_company_val,amazon_link=m.amazon_link,flipkart_link=m.flipkart_link )
                product.save()
                i+=1
            except Exception as e:
                print("got the error while saving",end='')
                print(e)
        else:
            # smiluation
            i+=1
    print(f'items saved in db {i}')

'''
mList= mergeList(deserialiseTheListFromCSV("./csvs/flipkart-django-2_pages-realme phones.csv"),deserialiseTheListFromCSV("./csvs/amazon-django-2_pages-realme phones.csv"),categoryType='phones')
print("len of intersection item: {}".format(len(mList)))
saveToDB(mList)

saveTheMergeListIntoCSV(mList,"./csvs/merged-product-amaon-flipkart.csv")
'''