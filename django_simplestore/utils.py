import traceback
import uuid
from itertools import chain

from django.db.models import ForeignKey

from django_simplestore.models import Cart

def model_to_dict(instance, fields=None, exclude=None):# pragma: no cover
    """
    Returns a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, only the named
    fields will be included in the returned dict.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned dict, even if they are listed in
    the ``fields`` argument.
    """
    # avoid a circular import
    from django.db.models.fields.related import ManyToManyField
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.virtual_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, ManyToManyField):
            # If the object doesn't have a primary key yet, just use an empty
            # list for its m2m fields. Calling f.value_from_object will raise
            # an exception.
            if instance.pk is None:
                data[f.name] = []
            else:
                # MultipleChoiceWidget needs a list of pks, not object instances.
                qs = f.value_from_object(instance)
                if qs._result_cache is not None:
                    data[f.name] = [item.pk for item in qs]
                else:
                    data[f.name] = list(qs.values_list('pk', flat=True))
        elif isinstance(f,ForeignKey):
            try:
                data[f.name] = model_to_dict(getattr(instance,f.name))
            except (TypeError,ValueError):
                data[f.name] = f.value_from_object(instance)
        else:
            data[f.name] = f.value_from_object(instance)
    return data


def get_cart(request):
    request.session['uuid'] = request.session.get('uuid',str(uuid.uuid4()))
    cart,created = Cart.objects.get_or_create(owner=request.session['uuid'],closed=False)
    if created:
        cart.save()
    return cart

def get_cart_dict(request):
    if isinstance(request,Cart):
        cart = request
    else:
        cart = get_cart(request)
    if not cart.items.all():
        item_list = []
    else:
        item_list = [model_to_dict(item) for item in cart.items.all()]
    total_cost= cart.total_cost() #, "total cost for"
    total_count =  cart.total_count() #, "items in cart"

    return {"total_count":total_count,
            "total_cost":total_cost,"cart_items":item_list,
            "uuid":cart.owner,'raw_cart':model_to_dict(cart)}