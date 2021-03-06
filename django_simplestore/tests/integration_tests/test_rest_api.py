from django.test import TestCase
import json
from django_simplestore.models import Product



class APIEndpointTests(TestCase):
    def test_get_empty_cart(self):
        result = self.client.get("/api/v0/cart")
        json_result = json.loads(result.content)
        self.assertEqual(json_result["total_cost"],0)
        self.assertEqual(json_result["total_count"],0)
        self.assertEqual(json_result["uuid"],result.wsgi_request.session["uuid"])

    def test_add_product(self):
        product = Product(product_name="Test1",product_cost=2.23,product_ingredients="",product_description="")
        product.save()
        result = self.client.get("/api/v0/cart/add/%s"%product.pk)
        json_result = json.loads(result.content)
        self.assertEqual(json_result["status"],"OK")
        self.assertEqual(json_result["total_cost"],product.product_cost)
        self.assertEqual(json_result["total_count"],1)
    def test_bad_product(self):
        result = self.client.get("/api/v0/cart/add/1")
        json_result = json.loads(result.content)
        self.assertEqual(json_result["status"],"Fail")
        self.assertEqual(json_result["total_cost"],0)
        self.assertEqual(json_result["total_count"],0)
    def test_append_product(self):
        self.test_add_product()
        product = Product(product_name="Test2",product_cost=20.50,product_ingredients="",product_description="")
        product.save()
        result = self.client.get("/api/v0/cart/add/%s"%product.pk)
        json_result = json.loads(result.content)
        self.assertEqual(json_result["status"],"OK")
        self.assertEqual(json_result["total_cost"],product.product_cost+2.23)
        self.assertEqual(json_result["total_count"],2)
    def test_update_product(self):
        self.test_add_product()
        result = self.client.get("/api/v0/cart/update/1/3")
        json_result = json.loads(result.content)
        self.assertEqual(json_result["status"],"OK")
        self.assertEqual(json_result["total_cost"],2.23*3)
        self.assertEqual(json_result["total_count"],3)

        self.assertEqual(len(json_result["cart_items"]),1)
    def test_update_nonexisting(self):
        result = self.client.get("/api/v0/cart/update/1/3")
        json_result = json.loads(result.content)
        self.assertEqual(json_result['status'],'Fail')
        self.assertEqual(json_result["total_cost"],0)
        self.assertEqual(json_result["total_count"],0)




