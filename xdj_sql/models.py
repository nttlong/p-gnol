def table(table_name):
    ret = __table_wrapper__(table_name)
    return ret.wrapper

class __table_wrapper__(object):
    def __init__(self,table_name):
        self.__table_name__ = table_name
        self.__lookup_fields__ ={}

    def get_fields(self,dct,_fields):
        from django.db import models as dj_models
        for x in dct.items():

            obj = x[1]
            if hasattr(obj,"name"):
                field_name = obj.name or x[0]
            else:
                field_name = x[0]
            if field_name.__len__()>4 and field_name[0:2]=="__" and field_name[field_name.__len__()-2:field_name.__len__()] =="__":
                pass
            else:
                if isinstance(obj,TextField):
                    _fields.update({
                        field_name: dj_models.TextField(
                            name = field_name,
                            max_length = obj.max_len,
                            null = not obj.require,
                            unique = obj.unique
                        )
                    })
                elif isinstance(obj, DateField):
                    _fields.update({
                        field_name: dj_models.DateField(
                            name=field_name,
                            null=not obj.require,
                            unique=obj.unique
                        )
                    })
                elif isinstance(obj, NumberField):
                    _fields.update({
                        field_name: dj_models.FloatField(
                            name=field_name,
                            null=not obj.require,
                            unique=obj.unique
                        )
                    })
                elif isinstance(obj,IntegerField):
                    _fields.update({
                        field_name: dj_models.IntegerField(
                            name=field_name,
                            null=not obj.require,
                            unique=obj.unique
                        )
                    })

                elif isinstance(obj,CharField):
                    _fields.update({
                        field_name: dj_models.CharField(
                            name=field_name,
                            null=not obj.require,
                            unique=obj.unique,
                            max_length=obj.max_len
                        )
                    })
                elif isinstance(obj,BoolField):
                    _fields.update({
                        field_name: dj_models.BooleanField(
                            name=field_name,
                            null=not obj.require,
                            unique=obj.unique,
                            max_length=obj.max_len
                        )
                    })
                elif isinstance(obj,LookupField):
                    _fields.update({
                        field_name: dj_models.ForeignKey(
                            to=obj.__model__,
                            to_field=obj.__foreign_fields__,
                            db_column=obj.__local_fields__,
                            on_delete=None
                        )
                    })
                    class runner():
                        def __init__(self,fn_name):
                            self.fn_name = fn_name

                        def run(self):
                            from xdj_sql import Fields
                            return getattr(Fields, self.fn_name)
                    self.__lookup_fields__.update({
                        field_name: runner(field_name)
                    })
                else:
                    _fields.update({
                        field_name: obj
                    })

        return _fields

    def get_default_value_fields(self,dct,_fields):
        from django.db import models as dj_models
        for x in dct.items():
            obj = x[1]
            if hasattr(obj, "name"):
                field_name = obj.name or x[0]
            else:
                field_name = x[0]

            default_value = None
            if hasattr(obj,"default_value"):
                default_value = obj.default_value
            if default_value:
                _fields.update({
                    field_name:default_value
                })
        return _fields

    def get_require_fields(self,dct,_fields):
        from django.db import models as dj_models
        for x in dct.items():
            obj = x[1]
            if hasattr(obj, "name"):
                field_name = obj.name or x[0]
            else:
                field_name = x[0]

            default_value = None
            if hasattr(obj,"require") and obj.require:
                _fields.update({
                    field_name: obj
                })
        return _fields

    def wrapper(self,*args,**kwargs):
        import types

        _fields = {}
        _default_values_fields = {}
        _require_fields = {}

        from .utils import create_model

        _fields = self.get_fields(args[0].__dict__, _fields)
        _default_values_fields = self.get_default_value_fields(args[0].__dict__, _default_values_fields)
        _require_fields = self.get_require_fields(args[0].__dict__,_require_fields)
        __bases__ = args[0].__bases__
        while __bases__.__len__() >0:
            _dct = __bases__[0].__dict__
            _fields = self.get_fields(_dct, _fields)
            _default_values_fields = self.get_default_value_fields(_dct, _default_values_fields)
            _require_fields = self.get_require_fields(_dct, _require_fields)
            __bases__ = __bases__[0].__bases__
        # for cls in args[0].__bases__:
        #     _fields = self.get_fields(cls.__dict__, _fields)
        #     _default_values_fields = self.get_default_value_fields(cls.__dict__,_default_values_fields)
        #     _require_fields = self.get_require_fields(cls.__dict__, _require_fields)
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
        ret.__default_values_fields__ = _default_values_fields
        ret.__require_fields__ = _require_fields
        ret.__lookup_fields__= self.__lookup_fields__
        ret.__origin_class__ = args[0]

        return ret



class Base(object):

    def __init__(self):
        self.__model__ = None
        self.__default_values_fields__ = None
        self.__require_fields__ = None
        self.__lookup_fields__ = {}
        self.__origin_class__ = None

    def __getattr__(self, item):
        call_fn = self.__lookup_fields__.get(item,None)
        if call_fn:
            return call_fn.run
        if item.__len__()>4:
            if item[0:2] == "__" and item[item.__len__()-2:item.__len__()] == "__":
                return self.__dict__.get(item,None)
        if hasattr(self.__model__,item):
            from xdj_sql import Fields
            return getattr(Fields,item)
        else:
            raise (Exception("{0} was not found in {1}".format(
                item, self.__origin_class__
            )))

    def __call__(self, *args, **kwargs):
        pass

    def __lshift__(self, other):
        data = {}
        if isinstance(self.__default_values_fields__, dict):
            for k, v in self.__default_values_fields__.items():
                val = v
                if callable(v):
                    val = v()

                data.update({
                    k: val
                })
        from xdj_sql import exceptions
        from xdj_sql.utils import __field__
        if isinstance(other,tuple):
            for x in other:
                data.update(x)
        elif isinstance(other, dict):
            for k,v in other.items():
                if isinstance(k, __field__):
                    data.update({
                        k.__f_name__:v
                    })
        else:
            raise Exception("Can not create instance with {0}".format(
                type(other)
            ))

        if isinstance(self.__require_fields__,dict):
            _required_fields = []
            for k,v in self.__require_fields__.items():
                if isinstance(v,TextField):
                    if data.get(k,"") == "":
                        _required_fields.append(k)
                elif not data.get(k, None):
                        _required_fields.append(k)
            if _required_fields.__len__()>0:
                raise exceptions.RequireValue("Missing fields {0}".format(_required_fields),_required_fields)

        return self.__model__.objects.create(**data)



class BaseField(object):
    def __init__(self,name=None,unique=False,max_len=255,require=False, default_value = None):
        self.name = name
        self.unique = unique
        self.max_len = max_len
        self.require = require
        self.default_value = default_value
        self.data_type = None


class TextField(BaseField):
    def __init__(self,name=None,max_len=45,unique=False, require = False, default_value = None):
        super(TextField,self).__init__(name,unique,max_len,require, default_value = default_value)


class CharField(BaseField):
    def __init__(self,name=None,max_len=45,unique=False, require = False, default_value = None):
        super(CharField,self).__init__(name,unique,max_len,require, default_value = default_value)

class DateField(BaseField):
    def __init__(self,name=None,unique=False, require = False, default_value = None):
        super(DateField,self).__init__(name,unique,max_len= None,require=require, default_value = default_value)


class NumberField(BaseField):

    def __init__(self, name=None, unique=False, require = False, default_value = None):
        super(NumberField, self).__init__(name,unique,max_len = None,require=require, default_value = default_value)

class IntegerField(BaseField):

    def __init__(self, name=None, unique=False, require = False, default_value = None):
        super(IntegerField, self).__init__(name,unique,max_len = None,require=require, default_value = default_value)

class BoolField(BaseField):

    def __init__(self, name=None, unique=False, require = False, default_value = None):
        super(BoolField, self).__init__(name,unique,max_len = None,require=require, default_value = default_value)

class LookupField():
    def __init__(self,model, local_fields, foreign_fields):
        self.__model__ = model
        self.__local_fields__ = local_fields
        self.__foreign_fields__= foreign_fields


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

    @staticmethod
    def integer(name=None,unique=False,require=False, default_value = None):
        return IntegerField(name, unique, require, default_value)

    @staticmethod
    def varchar(name=None,max_len = None, unique=False,require=False, default_value = None):
        return CharField(name=None,max_len = None, unique=False,require=False, default_value = None)

    @staticmethod
    def boolean(name=None,  unique=False, require=False, default_value=None):
        return BoolField(name=None, unique=False, require=False, default_value=None)

    @staticmethod
    def lookup(local_fields,foreign_fields):
        def wrapper(*args,**kwargs):
            model = args[0](None)
            return LookupField(
                model.__model__,
                local_fields=local_fields,
                foreign_fields = foreign_fields
            )

        return wrapper




