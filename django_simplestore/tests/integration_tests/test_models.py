from django.test import TestCase
from django_simplestore.models import Product
from django_simplestore.utils import get_cart, get_cart_dict


class FakeRequest:
    session = {'uuid':'hello_world'}
class CartTests(TestCase):
    def setUp(self):
        self.cart = get_cart(FakeRequest())
        self.product = Product(product_name="test1",product_description="",product_cost=2.25,product_ingredients="")
        self.product.save()
        self.product2 = Product(product_name="test2",product_description="",product_cost=2.50,product_ingredients="")
        self.product2.save()
    def test_add_item_manually(self):
        self.cart.add_product(self.product)
        self.cart.save()
        self.assertEqual(self.cart.total_count(),1)
        item = self.cart.items.first()
        self.assertEqual(item.product,self.product)
        self.assertEqual(item.quantity,1)
        self.assertEqual(item.cart,self.cart)
    def test_cart_to_dict(self):
        expect_cart = {'total_cost': 0, 'total_count': 0,
                       'raw_cart': {
                           'owner': 'hello_world', 'status': 'NEW', u'id': 1, 'closed': False, 'timestamp': 0
                       },
                       'cart_items': [], 'uuid': 'hello_world'}
        self.assertEqual(get_cart_dict(self.cart),expect_cart)
    def test_add_item_append(self):
        self.cart.add_products(self.product, self.product)
        self.cart.save()
        self.assertEqual(self.cart.total_count(),2) # two total items
        self.assertEqual(self.cart.items.count(),1) #only one unique item
        item = self.cart.items.first()
        self.assertEqual(item.product,self.product)
        self.assertEqual(item.quantity,2)
        self.assertEqual(item.cart,self.cart)

    def test_two_items(self):
        self.cart.add_products(self.product, self.product2)
        self.cart.save()
        self.assertEqual(self.cart.total_count(),2) # two total items
        self.assertEqual(self.cart.items.count(),2) #two unique items
        items = set(self.cart.items.all())
        pks = set(item.pk for item in items)
        self.assertEqual(pks.intersection([self.product.pk,self.product2.pk]),pks)
        for i,item in enumerate(items):
            self.assertEqual(item.quantity,1)
            self.assertEqual(item.cart,self.cart)

    def test_two_items_append(self):
        self.cart.add_products(self.product, self.product2)
        self.cart.add_products(self.product, self.product2)
        self.cart.save()
        self.assertEqual(self.cart.total_count(),4) # four total items
        self.assertEqual(self.cart.items.count(),2) #two unique items
        items = set(self.cart.items.all())
        pks = set(item.pk for item in items)
        self.assertEqual(pks.intersection([self.product.pk,self.product2.pk]),pks)
        for item in items:
            self.assertEqual(item.quantity,2)
            self.assertEqual(item.cart,self.cart)
        expected_cart = {'total_cost': 9.5, 'total_count': 4,
                         'raw_cart': {
                             'owner': 'hello_world', 'status': 'NEW', u'id': 1, 'closed': False, 'timestamp': 0
                         },
                         'cart_items': [
                             {'product': {
                                 'background_image': u'', 'title_color': u'#000000', 'product_name': u'test1',
                                 'product_cost': 2.25, 'product_description': u'', 'product_ingredients': u'',
                                 u'id': 1
                                }, u'id': 1,
                                 'cart': {
                                     'owner': 'hello_world', 'status': 'NEW', u'id': 1, 'closed': False,
                                     'timestamp': 0},
                                 'quantity': 2
                             },
                             {'product': {
                                 'background_image': u'', 'title_color': u'#000000', 'product_name': u'test2',
                                 'product_cost': 2.5, 'product_description': u'', 'product_ingredients': u'', u'id': 2
                                 },
                                 u'id': 2, 'cart': {
                                    'owner': 'hello_world', 'status': 'NEW', u'id': 1, 'closed': False, 'timestamp': 0
                                 }, 'quantity': 2
                             }
                         ], 'uuid': 'hello_world'}
        self.assertEqual(get_cart_dict(self.cart),expected_cart)