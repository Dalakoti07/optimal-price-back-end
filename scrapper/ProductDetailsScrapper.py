# scarps the product detail from flipkart page

import argparse
import time
from bs4 import BeautifulSoup
from requests import get
import sys
import csv
import json
import sys, os
import re
# comment below line for when running from main 

def readConfigFile(callFromMain):
    JsonFile=None
    if callFromMain:
        with open('./ecommerceClassesConfig.json') as f:
            JsonFile = json.load(f)
    else:
        with open('./scrapper/ecommerceClassesConfig.json') as f:
            JsonFile = json.load(f)
    return JsonFile

def saveTheHTML(html,fileName):
    with open(fileName, 'w', newline='') as htmlFile:
        htmlFile.write(html)
def readHTML(fileName):
    with open(fileName,'r') as htmlFile:
        return htmlFile.read()
# TODO scrap the reviews also
def getTheSpecs(classNameAttributes,html):
    specsDict={}
    specCard=html.find('div',href=False,attrs={'class':classNameAttributes['card']})
    for each_sub_spec_card in specCard.findAll('div',href=False,attrs={'class':classNameAttributes['subcard']}):
        try:
            subSpecTitle=each_sub_spec_card.find('div',href=False,attrs={'class':classNameAttributes['sub-spec-title']}).text
            innerDict={}
            sepcTable=each_sub_spec_card.find('table',href=False,attrs={'class':classNameAttributes['table']})
            rows = sepcTable.findChildren(['tr'])
            for row in rows:
                cells = row.findChildren('td')
                # obtain data from cells
                if len(cells)==2:
                    feature=cells[0].text
                    detail=cells[1].ul.li.text
                    innerDict[feature]=detail
                else:
                    continue
            specsDict[subSpecTitle]=innerDict
        except Exception as e:
            continue
    return specsDict

def getTheReviews(classNameAttributes,html):
    review_dict={}
    i=1
    for each_review_card in html.findAll('div',href=False,attrs={'class':classNameAttributes['review-box']}):
        try:
            review_title =each_review_card.find('p',href=False,attrs={'class':classNameAttributes['review-title']})
            review_title=review_title.text if review_title else ''
            review_rating =each_review_card.find('div',href=False,attrs={'class':classNameAttributes['review-rating']})
            review_rating=review_rating.text if review_rating else ''
            review_content =each_review_card.find('div',href=False,attrs={'class':classNameAttributes['review-content']}).div.div
            review_content=review_content.text if review_content else ''
            reviever_details =each_review_card.find('div',href=False,attrs={'class':classNameAttributes['reviever-details']})
            # get name and location
            if reviever_details:
                ptags=reviever_details.findAll('p',href=False)
                reviever_name=ptags[0].text
                reviever_time_ago=ptags[2].text

                review_dict["review-{}".format(i)]={
                    "title":review_title,
                    "rating":review_rating,
                    "content":review_content,
                    "given_by":reviever_name,
                    "when_given":reviever_time_ago
                }
                i+=1
        except Exception as e:
            continue

    return review_dict

def getTheImages(classNameAttributes,html):
    imagesDict={}
    allImages=html.findAll('div',href=False,attrs={'class':classNameAttributes['image-div']})
    # take 5 images only
    try:
        allImages=allImages[0:6]
        i=1
        for image in allImages:
            imagesDict["image-{}".format(i)]=re.search('https://[a-z,0-9,\.,\/,\-,\?,\=]*',image["style"]).group(0)
            i=i+1
        return imagesDict
    except Exception as e:
        return imagesDict

#function used for scrapping in getthedata working for only mobiles
def scrapTheDetails(driver,url,callFromMain=False):    
    if not url:
        return None,None,None
    print("fetching the details from url..........{}".format(url))
    if driver:
        try :
            driver.get(url)
        except Exception as e:
            print("got an dirver exception return")
            return None,None,None
        time.sleep(1)
        html_soup = BeautifulSoup(driver.page_source, 'html.parser')
    else:
        # when running from main
        htmlPage= readHTML("./scrapper/htmls/realmedetails.html")
        html_soup = BeautifulSoup(htmlPage, 'html.parser')
    
    # saveTheHTML(driver.page_source,"./htmls/realmedetails.html")

    classNameAttributes=readConfigFile(callFromMain)
    classNameAttributes=classNameAttributes["flipkart"]['product-details']

    specsDict= getTheSpecs(classNameAttributes,html_soup)
    imagesDict= getTheImages(classNameAttributes,html_soup)
    reviewsDict=getTheReviews(classNameAttributes,html_soup)

    if callFromMain:
        saveTheResultsToFile('csvs/details-phone.csv',specsDict)
    json_spec_all = json.dumps(specsDict, indent = 4)
    json_images=json.dumps(imagesDict,indent=4)
    json_reviews=json.dumps(reviewsDict,indent=4)

    # print('reviews are {} '.format(json_reviews))
    return (json_spec_all,json_images,reviewsDict)
    
    # print('one url '+listOfProducts[0].image_url+listOfProducts[4].image_url)

if __name__ == "__main__":
    from ScrapperUtils import saveTheResultsToFile

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="enter the item name you want to search on flipkart",type=str)
    args = parser.parse_args()

    print("main function directly called and its is running and keyword searched :"+args.url)
    driver=None
    '''
    service = Service('./driver')
    service.start()
    driver=webdriver.Remote(service.service_url) 
    '''
    scrapTheDetails(driver,args.url,callFromMain=True)
    # driver.close()
else:
    print("Executed when imported")

