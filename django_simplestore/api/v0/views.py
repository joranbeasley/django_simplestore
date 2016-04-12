import json

from django.http import  JsonResponse
from django.db.models.base import ObjectDoesNotExist
from django_simplestore.models import Product, CartItem
from django_simplestore.utils import get_cart, get_cart_dict


def add_product_to_cart(request,product_id):
    data={}
    try:
        product = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        data = {"status":"Fail"}
    else:
        data = {"status":"OK"}
        cart = get_cart(request)
        cart.add_product(product)
        cart.save()
    finally:
        data.update(get_cart_dict(request))
        return JsonResponse(data)
def update_cart(request,product_id,qty):
    data={}
    try:
        product = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        data = {"status":"Fail"}
    else:
        data = {"status":"OK"}
        cart = get_cart(request)
        item,created = CartItem.objects.get_or_create(cart=cart,product=product)
        if not created:
            item.quantity += 1
        item.save()
    finally:
        data.update(get_cart_dict(request))
        return JsonResponse(data)
def get_cart(request):
    return JsonResponse(get_cart_dict(request))
