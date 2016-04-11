import os

import sys
from django.test import TestCase
from django_simplestore.models import Product,Page

class ProductTests(TestCase):
    def test_sanity(self):
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'],'django_simplestore.settings')
    def test_product_unicode(self):
        product = Product(product_name="Test Product1",product_cost=2.25,product_description="Test Description",product_ingredients="")
        self.assertEqual(unicode(product),"<Product name='Test Product1' cost='$2.25'>")


class PageTests(TestCase):
    def test_page_unicode(self):
        page = Page(title="Test Page",slug="test1",page_html="<h1>Test</h1>")
        self.assertEqual(unicode(page),"test1")
