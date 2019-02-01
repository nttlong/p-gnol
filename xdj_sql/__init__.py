from argparse import _ActionsContainer
from django.db.utils import IntegrityError
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
        from . models import Base as B
        self.__xdj_model__ = None
        if isinstance(model, B):
            self.__model__ = model.__model__
            self.__xdj_model__ = model
        elif issubclass(model, Model):
            self.__model__ = model
        else:
            raise Exception("'model' is invalid. The model must be {0} or {1}".format(
                Model,B
            ))
        self.__fields__ = {}
        self.__where__ = None
        self.__select_related__ = []
        self.__sort__ = []

    def select(self,*args,**kwargs):
        from django.db.models.fields import DeferredAttribute
        from . utils import __field__, check_is_str
        from . import __express_field__

        if args.__len__()>0:
            for x in args:
                if isinstance(x,DeferredAttribute):
                    self.__fields__.update({
                        x.field_name: 1
                    })
                elif check_is_str(x):
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
        from xdj_sql.utils import __field__
        if args.__len__()>0:
            for x in args:
                try:
                    if issubclass(x,Model):
                        self.__select_related__.append(
                            x.__name__
                        )
                except TypeError as ex:
                    self.__select_related__.append(
                        x.__f_name__
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

    def insert(self,*args,**kwargs):
        from xdj_sql.utils import __field__
        data = {}
        for x in args:
            if isinstance(x,dict):
                for k,v in x.items():
                    data.update({
                        k: v
                    })
        try:
            x = self.__model__.objects.create(**data)
            return x
        except Exception as ex:
            from xdj_sql.error_description import get_error
            ret = get_error(self.__model__._meta.db_table,ex)
            return None, ret

    def update(self,*args,**kwargs):
        from xdj_sql.utils import __field__
        if self.__where__:
            items = self.__model__.objects.filter(self.__where__).all()
            if items.__len__()>0:
                item = items[0]
                for x in args:
                    if isinstance(x,dict):
                        for k,v in x.items():
                            setattr(item, k, v)
                try:
                    item.save()
                except Exception as ex:
                    from xdj_sql.error_description import get_error
                    ret = get_error(self.__model__._meta.db_table, ex)
                    return None, ret
        return item, None


    def join(self,to,local_fields, foreign_fields):
        from django.db import models as dj_models
        class obj(object):
            pass
        link = obj()
        link.nullable = None
        # link_type = obj()
        # link_type.join_type = 'INNER JOIN'
        link.table_name = to.__model__.__name__
        link.parent_alias = to.__model__._meta.db_table
        link.join_type = 'INNER JOIN'
        INNER = 'INNER JOIN'
        LOUTER = 'LEFT OUTER JOIN'
        # _qr = self.__model__.objects.all().query
        # _qr.alias_map.update({
        #     link.parent_alias: link_type
        # })
        # _qr.join(link)
        #Depts = models.ForeignKey(to=Depts.__model__,to_field="id",db_column="DeptId")

        lookup_field = dj_models.ForeignKey(
            to=to.__model__,
            to_field=foreign_fields.__f_name__,
            db_column=local_fields.__f_name__,
            related_name="Depts"



            )
        lookup_field.concrete = True
        lookup_field.model = to.__model__
        lookup_field.column = local_fields.__f_name__
        lookup_field.attname = local_fields.__f_name__
        self.__model__._meta.add_field(lookup_field)
        print (self.__model__.objects.all())
        # self.__model__.objects.all().query.join(link)
        # fx = self.__model__.objects.all().query.join(link)

        pass


class obj_data(object):
    def __init__(self,data):
        self.__dict__.update(data)






Fields = utils.Fields
from . import funcs as Funcs
from . models import table
from . models import fields
