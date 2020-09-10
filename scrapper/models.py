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
    amazon_link=models.CharField(max_length=500,null=True,default='')
    flipkart_link=models.CharField(max_length=500,null=True,default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)

class Deals(models.Model):
    sales_link=models.CharField(max_length=500,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sales_image_link=models.CharField(max_length=500,null=False)
    
# specially for mobiles
class ProductDetails(models.Model):
    # TODO get the images(flipkart) and reviews (flipkart)
    product_link=models.CharField(max_length=500,null=False,default='')
    # product=models.OneToOneField(Product,on_delete=models.CASCADE)

    # general
    in_the_box=models.CharField(max_length=200,blank=True,default='')
    model_number=models.CharField(max_length=20,blank=True,default='')
    model_name=models.CharField(max_length=20,blank=True,default='')
    color=models.CharField(max_length=20,blank=True,default='')
    browser_type=models.CharField(max_length=20,blank=True,default='')
    sim_type=models.CharField(max_length=20,blank=True,default='')
    hybrid_sim_slot=models.BooleanField(blank=True,default=False)
    touch_screen=models.BooleanField(blank=True,default=False)
    OTG_compatible=models.BooleanField(blank=True,default=False)
    sound_enhancement=models.BooleanField(blank=True,default=False)    
    sar_value=models.CharField(max_length=50,blank=True,default='')
    
    # display feature
    display_size=models.CharField(max_length=50,blank=True,default='')
    resolution=models.CharField(max_length=50,blank=True,default='')
    resolution_type=models.CharField(max_length=10,blank=True,default='')
    other_display_feature=models.CharField(max_length=10,blank=True,default='')

    # os and processot features
    operating_system=models.CharField(max_length=20,blank=True,default='')
    processor_type=models.CharField(max_length=50,blank=True,default='')
    processor_core=models.CharField(max_length=20,blank=True,default='')
    primary_clock_speed=models.CharField(max_length=10,blank=True,default='')
    secondary_clock_speed=models.CharField(max_length=10,blank=True,default='')
    operating_frequency=models.CharField(max_length=100,blank=True,default='')

    # memory and storage features
    internal_storage=models.CharField(max_length=10,blank=True,default='')
    ram=models.CharField(max_length=10,blank=True,default='')
    supported_memory_card_type=models.CharField(max_length=20,blank=True,default='')
    memory_card_slot_type=models.CharField(max_length=20,blank=True,default='')

    # camera features
    primary_camera_available=models.BooleanField(blank=True,default=False)
    primary_camera=models.CharField(max_length=50,blank=True,default='')
    primary_camera_features=models.CharField(max_length=1000,blank=True,default='')
    secondary_camera_available=models.BooleanField(blank=True,default=False)
    secondary_camera=models.CharField(max_length=50,blank=True,default='')
    secondary_camera_features=models.CharField(max_length=1000,blank=True,default='')
    flash=models.CharField(max_length=20,blank=True,default='')
    flash_rate=models.CharField(max_length=100,blank=True,default='')
    dual_camera_lens=models.CharField(max_length=20,blank=True,default='')

    # connectivity features
    networking_type=models.CharField(max_length=50,blank=True,default='')
    supported_network=models.CharField(max_length=100,blank=True,default='')
    internet_connectivity=models.CharField(max_length=50,blank=True,default='')
    three_g_speed=models.CharField(max_length=20,blank=True,default='')
    gprs=models.BooleanField(blank=True,default=False)
    preinstalled_browser=models.CharField(max_length=1000,blank=True,default='')
    micro_usb_port=models.BooleanField(blank=True,default=False)
    bluetooth_support=models.BooleanField(blank=True,default=False)
    bluetooth_version=models.CharField(max_length=10,blank=True,default='')
    wifi=models.BooleanField(blank=True,default=False)
    wifi_version=models.CharField(max_length=20,blank=True,default='')
    usb_connectivity=models.BooleanField(blank=True,default=False)
    edge=models.BooleanField(blank=True,default=False)
    audio_jack=models.CharField(max_length=10,blank=True,default='')

    #TODO complete if interest prevails
    # skipping other details, multi media feature, battery and power feature

    # dimensions
    width=models.CharField(max_length=10,blank=True,default='')
    height=models.CharField(max_length=10,blank=True,default='')
    depth=models.CharField(max_length=10,blank=True,default='')
    weight=models.CharField(max_length=10,blank=True,default='')

    # warrenty
    warranty_summary=models.CharField(max_length=100,blank=True,default='')

    # list of image src
    product_images = ListCharField(
        base_field=CharField(max_length=500),
        size=6,
        max_length=(6 * 501)  # 6 * 10 character nominals, plus commas
    )

class Review(models.Model):
    reviewer_name=models.CharField(max_length=20,blank=False,default='')
    reviewer_address=models.CharField(max_length=20,blank=False,default='')
    review_title=models.CharField(max_length=20,blank=False,default='')
    ratings=models.IntegerField()
    content=models.CharField(max_length=500,blank=False,default='')
