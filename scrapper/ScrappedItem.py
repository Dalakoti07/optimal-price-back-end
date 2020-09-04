class ScrappedItem():
    def __init__(self, name, rating,image_url,price,href):
        self.name = name
        self.rating = rating
        self.image_url=image_url
        self.price=price
        self.href=href
    
    def __str__(self):
        return "name:{} and rating:{} \n".format(self.name,self.rating)
    def __repr__(self):
        return "name:{} and rating:{} \n".format(self.name,self.rating)

