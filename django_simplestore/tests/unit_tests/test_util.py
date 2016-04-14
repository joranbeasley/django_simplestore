import time

import datetime
from django.test import TestCase

from django_simplestore.constants import ONE_HOUR
from django_simplestore.models import ImageLister
from django_simplestore.utils import get_cart, get_cart_dict

class FakeRequest:
    session = {'uuid':'hello_world'}
class UtilTests(TestCase):

    def test_get_cart_known_uuid(self):

        cart = get_cart(FakeRequest())
        self.assertEqual(cart.owner,"hello_world")
    def test_cart_shipping_timer_unpaid(self):
        cart = get_cart(FakeRequest())
        self.assertFalse(cart.ready_for_ship())
        self.assertEqual(cart.ready_at(),"Not Paid!")
    def test_cart_shipping_timer_notready(self):
        cart = get_cart(FakeRequest())
        cart.timestamp = int(time.time())
        self.assertFalse(cart.ready_for_ship())
        format_string="%x %X"
        expect = datetime.datetime.fromtimestamp(cart.timestamp+ONE_HOUR*24).strftime(format_string)
        self.assertEqual(cart.ready_at(format_string),expect)
    def test_cart_shipping_timer_ready(self):
        cart = get_cart(FakeRequest())
        cart.timestamp = int(time.time())-ONE_HOUR*24-1
        self.assertTrue(cart.ready_for_ship())
        format_string="%x %X"
        expect = datetime.datetime.fromtimestamp(cart.timestamp+ONE_HOUR*24).strftime(format_string)
        self.assertEqual(cart.ready_at(format_string),expect)
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

    def test_bad_dirlister(self):
        x = list(ImageLister("./asdqqtwer","png"))
        self.assertTrue(x[0].startswith("Error:"))