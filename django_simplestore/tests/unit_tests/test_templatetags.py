

from django_simplestore.tests.util import TmplTestCase


class TemplateTagUnitTests(TmplTestCase):
    def test_product_render(self):
        rendered = self.render_template(
            '{% load product_render %}'
            '{% render_product product %}'
        ,{'product':{'product_name':'testProduct',"product_cost":2.33,"product_desc":"a product description... Test?"}})
        self.assertIn("testProduct",rendered,"Rendered Template(%r) Does not have the product_name"%rendered)