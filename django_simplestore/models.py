import os

from django.db.models import Model,CharField,TextField,FloatField,FileField,EmailField, ManyToManyField, ForeignKey, \
    IntegerField, BooleanField, OneToOneField
from django.contrib.admin import ModelAdmin,site,register
from colorfield.fields import ColorField
class ImageLister:
    def __init__(self,directory,extensions=None):
        self.directory = directory
        self.extensions = extensions
    def __iter__(self):
        def match_extension(n):
            return not self.extensions or any(n.lower().endswith(e.lower()) for e in self.extensions)
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

@register(Product)
class ProductAdmin(ModelAdmin):
    class Media:
        js = [
            'js/file_upload_select.js'
        ]
    fieldsets = (
        ('Product Background Image', {
             'fields': ('background_image',),
             'classes': ('file-select',)
             }
        ),
       ('Product Details', {
             'fields': ('product_name title_color product_cost product_description product_ingredients'.split())
             }
        ),
    )

class Page(Model):
    title=CharField(max_length=200)
    slug=CharField(primary_key=True,max_length=200)
    page_html = TextField(default="")
    def __unicode__(self):
        return self.slug

@register(Page)
class PageAdmin(ModelAdmin):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]