
from . import utils

class __alias_field__(object):

    def __init__(self, expr):
        self.__expr__ = expr

class __express_field__(object):

    def __init__(self,name, expr):
        self.__expr__ = expr
        self.__f_name__ = name

class qr(object):

    def __init__(self, model = None):
        from django.db.models import Model

        if model and not issubclass(model,Model):
            raise Exception("Invalid model. The model must be inherit from {0}".format(
                Model
            ))

        self.__model__ = model
        self.__fields__ = {}
        self.__where__ = None
        self.__select_related__ = []
        self.__sort__ = []

    def select(self,*args,**kwargs):
        from django.db.models.fields import DeferredAttribute
        from . utils import __field__
        from  . import __express_field__
        if args.__len__()>0:
            for x in args:
                if isinstance(x,DeferredAttribute):
                    self.__fields__.update({
                        x.field_name: 1
                    })
                elif type(x) in [str, unicode]:
                    self.__fields__.update({
                        x:1
                    })
                elif isinstance(x,__express_field__):
                    self.__fields__.update({
                        x.__f_name__: x
                    })
                elif isinstance(x, __field__):
                    if x.__alias__:
                        if not x.__expr__:
                            self.__fields__.update({
                                x.__f_name__: __alias_field__(x.__alias__)
                            })
                        else:
                            self.__fields__.update({
                                x.__f_name__: __express_field__(x.__f_name__,x.__expr__)
                            })
                    else:
                        self.__fields__.update({
                            x.__f_name__: 1
                        })
        return self

    def select_related(self,*args,**kwargs):
        from django.db.models import Model
        if args.__len__()>0:
            for x in args:
                if issubclass(x,Model):
                    self.__select_related__.append(
                        x.__name__
                    )
        return self

    def execute(self,model =None):
        from django.db.models import Model,F
        from xdj_sql import __express_field__
        from xdj_sql.utils import __field__

        if model and not issubclass(model,Model):
            raise Exception("Invalid model. The model must be inherit from {0}".format(
                Model
            ))
        if not model and not self.__model__:
            raise Exception("'model' must be set at __init__ or execute")
        if model:
            self.__model__ = model
        qr_set = self.__model__.objects
        if self.__select_related__.__len__()>0:
            for x in self.__select_related__:
                qr_set.select_related(x)
        if self.__where__:
            qr_set = qr_set.filter(self.__where__)

        selected_fields = []
        alias_fields = []
        for k, v in self.__fields__.items():
            if isinstance(v, __alias_field__):
                alias_fields.append((v.__expr__,F(k)))
                selected_fields.append(k)
            elif isinstance(v, __express_field__):
                alias_fields.append((k, v.__expr__))
            elif isinstance(v, __field__):
                if not v.__expr__:
                    selected_fields.append(k)
                else:
                    alias_fields.append((k, v.__expr__))
            else:
                selected_fields.append(k)

        # selected_fields = [k for k, v in self.__fields__.items()]

        if selected_fields.__len__() > 0:
            qr_set = qr_set.values(*selected_fields)
        if alias_fields.__len__() > 0:
            _annotate = {}
            for x in alias_fields:
                _annotate.update({
                    x[0]: x[1]
                })
            qr_set = qr_set.annotate(**_annotate)
            selected_fields = [x[0] for x in alias_fields]
            qr_set = qr_set.values(*selected_fields)
        if self.__sort__.__len__() > 0:
            _sort_ = []
            for x in self.__sort__:
                if x["asc"]:
                    _sort_.append(x["field"])
                    # qr_set = qr_set.order_by(x["field"])
                else:
                    _sort_.append("-" + x["field"])
                    # qr_set = qr_set.order_by("-"+x["field"])
            qr_set = qr_set.order_by(*_sort_)
        return qr_set

    def count(self):
        return self.execute().count()

    def limit(self,num):
        return self.execute()[:num]

    def skip(self,num):
        return self.execute()[num:]

    def sort(self,*args,**kwargs):
        from xdj_sql.utils import __field__
        if args.__len__()>0:
            for x in args:
                if isinstance(x,__field__):
                    if x.__sort__ == "desc":
                        self.__sort__.append(dict(
                            field=x.__f_name__,
                            asc = False
                        ))
                    else:
                        self.__sort__.append(dict(
                            field=x.__f_name__,
                            asc= True
                        ))
        return self


    def get_page(self,page_size,page_index):
        return self.execute()[page_size * page_index: page_size ]

    def first(self):
        return self.execute().first()

    def __iter__(self):
        return self.execute().all()

    def all(self):
        return self.execute().all()

    def where(self, expr):
        from .utils import __field__
        if isinstance(expr, __field__):
            self.__where__ = expr.__expr__
        else:
            raise Exception("Invalid data type of argument one\n"
                            "Example:\n"
                            "from xdj_sql import Fields\n"
                            "qr.where(Fields.Code=='aaa')")
        return self




Fields = utils.Fields
import funcs as Funcs
from . models import table
from . models import fields
