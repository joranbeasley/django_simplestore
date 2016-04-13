import os

import time

import datetime

from django.db.models import Model,CharField,TextField,FloatField, ForeignKey, IntegerField, BooleanField

from colorfield.fields import ColorField

from django_simplestore.constants import ONE_HOUR


class ImageLister:
    def __init__(self,directory,extensions=None):
        self.directory = directory
        self.extensions = extensions
    def __iter__(self):
        def match_extension(ext):
            return not self.extensions or any(ext.lower().endswith(e.lower()) for e in self.extensions)
        matches = os.listdir(self.directory)
        return ((m,m) for m in matches if match_extension(m))

class Product(Model):
    product_name=CharField(max_length=200)
    product_cost=FloatField(default=5.00)
    #: TODO implement title color ....
    title_color=ColorField(default="#000000") #: expect hex rgb value ie "#12aedd"
    product_description=TextField()
    product_ingredients=CharField(max_length=500)
    background_image=CharField(max_length=200,choices=ImageLister("./media","png jpg gif".split()))
    def __unicode__(self):
        return u"<Product name='%s' cost='$%0.2f'>"%(self.product_name,self.product_cost)



class Page(Model):
    title=CharField(max_length=200)
    slug=CharField(primary_key=True,max_length=200)
    page_html = TextField(default="")
    menu_order = IntegerField(default=None)
    def __unicode__(self):
        return self.slug



class Cart(Model):
    owner = CharField(max_length=200)
    closed = BooleanField(default=False)
    status = CharField(max_length=50,default="NEW")
    timestamp = IntegerField(default=0)
    def add_product(self,product):
        item,created = CartItem.objects.get_or_create(cart=self,product=product)
        if not created:
            item.quantity += 1
        item.save()
    def add_products(self,*products):
        for product in products:
            self.add_product(product)
    def ready_for_ship(self):
        return (time.time()-self.timestamp) > ONE_HOUR * 24 #: 24 hours! (in seconds)
    def ready_at(self,format_string = "%d%b%Y %H:%M"):
        return datetime.datetime.fromtimestamp(self.timestamp+3600*24).strftime(format_string)
    def total_count(self):
        return sum(item.quantity for item in self.items.all())
    def total_cost(self):
        return sum(item.total_cost() for item in self.items.all())


class CartItem(Model):
    product = ForeignKey(Product)
    quantity = IntegerField(default=1)
    cart = ForeignKey(Cart,related_name='items')
    def total_cost(self):
        return self.quantity*self.product.product_cost