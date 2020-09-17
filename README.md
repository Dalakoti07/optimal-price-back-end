product categories - 
    mobile
    electronics
    books
    fashion
    health
    computers

200 + items in each category

Products API
/product_api/products - all products

/product_api/reviews/{product-id} - a specific review (handle if no review exist)
/product_api/reviews/ - all reviews
/product_api/full_specs/{product-id} - a specific spec
/product_api/full_specs/ - all specs


filling db apis

Mobiles
    {{base_url}}/product_api/scrap?search=samsung phones&pages=5 (20 items)
    {{base_url}}/product_api/scrap?search=realme phones&pages=5 (49 items)
    {{base_url}}/product_api/scrap?search=motorola phones&pages=5  (13 items)
    {{base_url}}/product_api/scrap?search=oppo phones&pages=4 (22 items)
    {{base_url}}/product_api/scrap?search=nokia phones&pages=5 (22 items)
    {{base_url}}/product_api/scrap?search=htc phones&pages=2 (10 items)
    {{base_url}}/product_api/scrap?search=apple phones&pages=4 (24 items)
    {{base_url}}/product_api/scrap?search=asus phones&pages=4 (12 items)
    {{base_url}}/product_api/scrap?search=sony phones&pages=4 (3 items)

    try lenovo, asus, infinix ,sony (1 page only)

Fashion Men and Women
    {{base_url}}/product_api/scrap?search=montrez jackets female&pages=1  (26 item from amazon, and 0 item from flipkart (flipkart classid is changing ) )
    {{base_url}}/product_api/scrap?search=ben martin jacket male&pages=1 (50 item from amazon and flipkart)
    {{base_url}}/product_api/scrap?search=puma shoes&pages=1  (106 items combined )
    {{base_url}}/product_api/scrap?search=adidas shoes&pages=1 (108 - 58 from amazon and 50 flipkart)
    {{base_url}}/product_api/scrap?search=young trendz t shirt women&pages=1  (98 - 48 from each)
    {{base_url}}/product_api/scrap?search=young trendz t shirt men&pages=1  (96 - 46 and 50 each)
    {{base_url}}/product_api/scrap?search=Urban Fashion jeans men&pages=1  (60 from aamzon and 18 from flip)
    {{base_url}}/product_api/scrap?search=kotty jeans female&pages=1  (99 total)

Books
    {{base_url}}/product_api/scrap?search=self help books&pages=5 (23 items with comparison)
    
    correct these
    {{base_url}}/product_api/scrap?search=cbse previous years books&pages=3 ( ,0 from amazon, amzon has multi book in 1 row and thus cards are missing) 

Electronics
    Refrigerator
        {{base_url}}/product_api/scrap?search=samsung refrigerator&pages=3 (17 products) 
        {{base_url}}/product_api/scrap?search=LG refrigerator&pages=3 (10 products) 
        {{base_url}}/product_api/scrap?search=whirlpool refrigerator&pages=3 (21 products)
    Television search key LED
        samsung LED {{base_url}}/product_api/scrap?search=samsung televisions&pages=3 (30 products)
        lg LED {{base_url}}/product_api/scrap?search=LG televisions&pages=3 (18 products)
        panasonic {{base_url}}/product_api/scrap?search=panasonic televisions&pages=3 (25 products)
    Cameras
        FIXME canon and nikon camera details is crashing
        {{base_url}}/product_api/scrap?search=canon cameras&pages=3 (13 items)
        {{base_url}}/product_api/scrap?search=sony cameras&pages=3 (13 items)  
        {{base_url}}/product_api/scrap?search=nikon cameras&pages=3 (14 items)        
    headphones and speakers
        try brands

Laptops
    nomanclature is very different and hence very less intersection
    {{base_url}}/product_api/scrap?search=asus laptops&pages=3 (1 common)
    
6 categories:
    left and right comparison:
        men fashion
        women fashion
        fashion - shoes
        laptops

    amazon and flipkart and specs:
        electronics
        books
        mobiles

Implementation details / notes
Category decided by amazon is final and last say


Django ORM rules
