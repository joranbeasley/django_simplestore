import sys
from django.test import TestCase

from django_simplestore.utils import get_cart, get_cart_dict

class FakeRequest:
    session = {'uuid':'hello_world'}
class UtilTests(TestCase):

    def test_get_cart_known_uuid(self):

        cart = get_cart(FakeRequest())
        self.assertEqual(cart.owner,"hello_world")

    def test_get_cart_normal_request(self):
        response = self.client.get("/")
        request = response.wsgi_request
        cart = get_cart(request)
        self.assertEqual(cart.owner,request.session.get("uuid",""))
        self.assertEqual(cart.total_count(),0)
        self.assertEqual(cart.total_cost(),0)
        self.assertEqual(list(cart.items.all()),[])

    def test_get_cart_dict(self):
        cart = get_cart_dict(FakeRequest())
        expect_cart = {'total_cost': 0, 'total_count': 0,
                       'raw_cart': {'owner': 'hello_world', 'status': 'NEW', u'id': 1, 'closed': False, 'timestamp': 0},
                       'cart_items': [], 'uuid': 'hello_world'}
        self.assertEqual(cart,expect_cart)