
from django.contrib.admin import ModelAdmin,register
from django_simplestore.models import Page, Product


@register(Page)
class PageAdmin(ModelAdmin):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/js/tinymce_setup.js',
        ]


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