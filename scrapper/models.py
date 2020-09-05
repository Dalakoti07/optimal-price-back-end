from django.db import models
import uuid
# Create your models here.

# this model would be saved after all the data cleaning and preprocessing
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=50, blank=False, default='',unique=True)
    rating=models.CharField(max_length=20, blank=True, default='')
    image_url=models.CharField(max_length=500, blank=True, default='')
    # price=models.DecimalField(blank=False,max_digits=19, decimal_places=10)
    price=models.CharField(max_length=10, blank=False, default='')
    brand_name=models.CharField(max_length=20,blank=True,default='')
    # date_created=datetimeFeild()
    product_category=models.CharField(max_length=20,blank=False,default='')
    ecommerce_company=models.CharField(max_length=20,blank=False,default='')
    amazon_link=models.CharField(max_length=500,blank=True,default='')
    flipkart_link=models.CharField(max_length=500,blank=True,default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)