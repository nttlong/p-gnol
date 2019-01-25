def table(table_name):
    ret = __table_wrapper__(table_name)
    return ret.wrapper

class __table_wrapper__(object):
    def __init__(self,table_name):
        self.__table_name__ = table_name

    def get_fields(self,dct,_fields):
        from django.db import models as dj_models
        for x in dct.items():
            obj = x[1]
            if hasattr(obj,"name"):
                field_name = obj.name or x[0]
            else:
                field_name = x[0]
            if isinstance(obj,TextField):
                _fields.update({
                    field_name: dj_models.TextField(
                        name = field_name,
                        max_length = obj.max_len,
                        null = not obj.require,
                        unique = obj.unique
                    )
                })
            if isinstance(obj, DateField):
                _fields.update({
                    field_name: dj_models.DateField(
                        name=field_name,
                        null=not obj.require,
                        unique=obj.unique
                    )
                })
            if isinstance(obj, NumberField):
                    _fields.update({
                        field_name: dj_models.FloatField(
                            name=field_name,
                            null=not obj.require,
                            unique=obj.unique
                        )
                    })
        return _fields

    def wrapper(self,*args,**kwargs):
        import types

        _fields = {}

        from .utils import create_model

        _fields = self.get_fields(args[0].__dict__, _fields)
        for cls in args[0].__bases__:
            _fields = self.get_fields(cls.__dict__, _fields)


        model = create_model(
            self.__table_name__,
            _fields,
            app_label=args[0].__module__,
            options=dict(
                db_table=self.__table_name__
            )
        )

        ret = Base()

        ret.__model__ = model
        return ret



class Base(object):

    def __getattr__(self, item):
        from xdj_sql import Fields
        return getattr(Fields,item)


class BaseField(object):
    def __init__(self,name=None,unique=False,max_len=255,require=False, default_value = None):
        self.name = name
        self.unique = unique
        self.max_len = max_len
        self.require = require
        self.default_value = default_value


class TextField(BaseField):
    def __init__(self,name=None,max_len=45,unique=False, require = False, default_value = None):
        super(TextField,self).__init__(name,unique,max_len,require, default_value = default_value)



class DateField(BaseField):
    def __init__(self,name=None,unique=False, require = False, default_value = None):
        super(DateField,self).__init__(name,unique,max_len= None,require=require, default_value = default_value)


class NumberField(BaseField):

    def __init__(self, name=None, unique=False, require = False, default_value = None):
        super(NumberField, self).__init__(name,unique,max_len = None,require=require, default_value = default_value)

class fields():

    @staticmethod
    def text(name=None,max_len=None,unique=False,require=False, default_value = None):
        return TextField(name,max_len,unique,require,default_value)

    @staticmethod
    def date(name=None,unique=False,require=False, default_value = None):
        return DateField(name,unique,require, default_value)

    @staticmethod
    def number(name=None,unique=False,require=False, default_value = None):
        return NumberField(name,  unique, require, default_value)



