from django.conf.urls import url
from django_simplestore.api.v0.views import add_product_to_cart, get_cart_details, update_cart

urlpatterns = [
    url(r'^cart/add/(?P<product_id>[0-9]+)$', add_product_to_cart),
    url(r'^cart$', get_cart_details),
    url(r'^cart/update/(?P<product_id>[0-9]+)/(?P<qty>[0-9]+)$', update_cart),
]
