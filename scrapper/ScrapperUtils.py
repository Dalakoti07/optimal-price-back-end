from .ScrappedItem import ScrappedItem
import csv
def merge(amazonList,flipkartList):
    # merge the list
    mergedItems=[]
    
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

def serialiseTheScrappedPagesIntoCSV(productList,fileName):
    with open(fileName, 'w', newline='') as csvfile:
        if len(productList)==0:
            return
        csvWriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        print("len of product list which is being serialised is : "+str(len(productList)))
        for d in productList:
            # print("writing {}".format(d))
            name = d.name
            rating = d.rating
            image_url=d.image_url
            price=d.price
            href=d.href
            csvWriter.writerow( detail for detail in [name,rating,image_url,price,href])

def deserialiseTheListFromCSV():
    pass

# itemList=[ScrappedItem("p1","2","imageurl",21,"www.google.com"),ScrappedItem("p5","22","imageurl2",221,"www.youtube.com")]
# serialiseTheScrappedPagesIntoCSV(itemList,'./csvs/test.csv')