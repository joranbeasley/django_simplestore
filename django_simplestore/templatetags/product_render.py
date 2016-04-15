from django import template

register = template.Library()

@register.inclusion_tag("django_simplestore/partials/product.html")
def render_product(product):
    return {"product":product}