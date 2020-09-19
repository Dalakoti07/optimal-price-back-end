if __name__ == "__main__":
    from ScrappedItem import ScrappedItem
else:
    # call from django,
    # but it can be call from flipkart or amazon scrapper
    # comment it when not using django
    from .ScrappedItem import ScrappedItem
    from .models import Product,ProductDetail,Review
    pass

import csv
import json
from difflib import SequenceMatcher

def returnJsonResponseFromProductList(productList,totalTime):
    data=[]
    for p in productList:
        data.append({
            "name":p.name,
            "rating":p.rating,
            "image_url":p.image_url,
            "price":p.price,
            "brand_name":p.brand_name,
            "amazon_link":p.amazon_link,
            "flipkart_link":p.flipkart_link,
            "product_category":p.product_category
        })
    response={
        "time-taken":str(totalTime),
        "length":len(data),
        "data":data
    }
    return response


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
    # priority wise attributes
    # name - flip, rating -flip, imageurl flip else amazon
    # price -amazon, 
    name=fi.name if fi.name else ai.name
    name=name.strip()
    rating=fi.rating if fi.rating else (ai.rating.split('out')[0] if ai.rating else None)
    image_url=fi.image_url if not '.svg' in fi.image_url else ai.image_url
    amazon_price,flipkart_price=None,None
    try:
        if fi.price:
            flipkart_price=int(fi.price.replace('₹','').replace(',',''))
        if ai.price:
            amazon_price=int(ai.price.replace(',','').replace('₹',''))
    except Exception as e:
        print("Error in processing price ")
        print(e)

    item= ScrappedItem(name=name,rating=rating,image_url= image_url
        ,price= None,href=None)
    # adding extra attributes [item's brand_name, amazon_link,flipkart_link,product_category]
    item.brand_name=item.name.split(' ')[0]
    item.amazon_price=amazon_price
    item.flipkart_price=flipkart_price
    item.amazon_link=ai.href
    item.flipkart_link=fi.href
    item.product_category=categorytype
    # validate data before saving it in db
    return item

def pseudoMergeIt(itemList,ecommerce_site,categoryType):
    # in pseudo merge give indices (number) to each repeated, to avoid
    uniqueName={} 
    print('pseudo merging it ')
    finalizeItems=[]
    for item in itemList:
        # correcting the name
        newCorrectName=None
        if item.name in uniqueName.keys():
            uniqueName[item.name]+=1
            newCorrectName= item.name+" ({})".format(uniqueName[item.name])
        else:
            uniqueName[item.name]=1
            newCorrectName= item.name

        newItem= ScrappedItem(name=newCorrectName,rating=item.rating,image_url=item.image_url,price=item.price,href=None)
        newItem.brand_name=newItem.name.split(' ')[0]
        try:
            if ecommerce_site=='amazon':
                newItem.amazon_price=int(item.price.replace('₹','').replace(',',''))
                newItem.flipkart_price=None
                newItem.amazon_link=item.href
                newItem.flipkart_link=None
                newItem.ecommerce_company='amazon'
            else:
                newItem.amazon_price=None
                newItem.flipkart_price=int(item.price.replace('₹','').replace(',',''))
                newItem.flipkart_link=item.href
                newItem.amazon_link=None
                newItem.ecommerce_company='flipkart'
        except Exception as e:
            continue
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
            currentName=currentName[:50]
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
        if m.name==None:
            continue
        if save:
            try:
                ecommerce_company_val='both'
                if hasattr(m, 'ecommerce_company'):
                    ecommerce_company_val=m.ecommerce_company
                product =Product(name=m.name,rating=m.rating,image_url=m.image_url,
                                amazon_price=m.amazon_price,flipkart_price=m.flipkart_price,
                                brand_name=m.brand_name,product_category=m.product_category,
                                ecommerce_company=ecommerce_company_val,amazon_link=m.amazon_link,
                                flipkart_link=m.flipkart_link )
                product.save()
                i+=1
            except Exception as e:
                print("got the error while saving",end='')
                print(e)
        else:
            # smiluation
            i+=1
    print(f'items saved in db {i}')

def saveProductDetailsToDB(productObject,json_spec_all,json_images,reviewsDict):
    # save product details
    print('saving details to db')
    try:
        product_spec=ProductDetail(product= productObject,product_full_spec= json_spec_all,product_images=json_images)
        product_spec.save()
    except Exception as e:
        print('got error when saving details object {}'.format(e))

    print('saved producst spec to db')
    # save review
    for review in reviewsDict:
        try:
            review_object=Review(product=productObject,
                    reviewer_name= reviewsDict[review]['given_by'],
                    review_given_when=reviewsDict[review]['when_given'],
                    review_title=reviewsDict[review]['title'],
                    ratings= int (reviewsDict[review]['rating']),
                    content=reviewsDict[review]['content']
                )
            review_object.save()
        except Exception as e:
            print('got error when saving review object {}'.format(e))
    print('saved reviews to db')

'''
flipList=deserialiseTheListFromCSV("./csvs/amazon-django-3_pages-samsung refrigerator.csv")
amazonList=deserialiseTheListFromCSV("./csvs/flipkart-django-3_pages-samsung refrigerator.csv")

print("size of amz list:{} and size of flipkart list:{}".format(len(amazonList),len(flipList)))
mList= mergeList(flipList,amazonList,categoryType='electronics')
print("len of intersection item: {}".format(len(mList)))
# saveToDB(mList)

saveTheMergeListIntoCSV(mList,"./csvs/merged-reg-amazon-flipkart.csv")
'''