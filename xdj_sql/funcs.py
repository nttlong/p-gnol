def concat(*args,**kwargs):
    from . utils import __field__, check_is_str

    from django.db.models import Value
    from django.db.models.functions import Concat
    params = []
    if args.__len__()>0:
        for x in args:
            if isinstance(x, __field__):
                params.append(x.__f_name__)
            elif check_is_str(x):
                params.append(Value(x))
    return Concat(*params)


def contains(field,txt):
    """
    icontains
    :param field:
    :param txt:
    :return:
    """
    from django.db.models import Q

    from .utils import __field__
    if isinstance(field,__field__):
        if field.__f_name__.count("__icontains")==0:
            field.__f_name__ = "{0}__icontains".format(field.__f_name__)
            field.__expr__ = {
                field.__f_name__:txt
            }
            field.__expr__ = Q(**field.__expr__)
    return field
def call(fn,*args,**kwargs):
    from .utils import __field__
    from django.db.models import Value,F
    x = []
    for item in args:
        if isinstance(item,__field__):
            x.append(F( item.__f_name__))
        elif type(item).__module__ == "django.db.models.functions.base":
            x.append(item)
        else:
            x.append(Value(item))
    return fn(*x)