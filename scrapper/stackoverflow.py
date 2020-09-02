from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver=webdriver.Chrome('./driver')
driver.get('https://www.flipkart.com/search?q=rayban/ray-ban-wayfarer')
time.sleep(3)
soup=BeautifulSoup(driver.page_source,'html.parser')
url='"https://www.flipkart.com'
jobs = soup.find_all('div',{"class":"IIdQZO _1R0K0g _1SSAGr"})

for job in jobs:
    product_name = job.find('a',{'class':'_2mylT6'})
    product_name = product_name.text if product_name else "N/A"

    product_offer_price = job.find('div',{'class':'_1vC4OE'})
    product_offer_price = product_offer_price.text if product_offer_price else "N/A"

    product_mrp = job.find('div',{'class':'_3auQ3N'})
    product_mrp = product_mrp.text if product_mrp else "N/A"

    product_link = job.find('a',{'class':'_3dqZjq'})
    product_link = product_link.get('href') if product_link else "N/A"
    product_link = url+ product_link

    product_img =job.find('div',{'class':'_3ZJShS _31bMyl'}).find('img')['src']

    print('product name {}\nproduct offer price {}\nproduct mrp {}\nproduct link {}\nproduct image {}'.\
      format(product_name,product_offer_price,product_mrp,product_link,product_img))
    print('\n')