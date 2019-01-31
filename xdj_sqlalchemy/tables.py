
class __wrapper__():
    def __init__(self,table_name):
        self.__table_name__ = table_name
    def wrapper(self,*args,**kwargs):
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer, String, DateTime, Boolean
        from datetime import datetime

        from sqlalchemy import Sequence
        base = declarative_base()
        cls = args[0]
        field_names = [k for k,v in cls.__dict__.items() if not (k.__len__()>4 and k[0:2]=="__" and k[k.__len__()-2:k.__len__()]=="__")]
        # type("test", (base,),
        #      {"__tablename__": "test", "id": Column(Integer, Sequence('user_id_seq'), primary_key=True)})
        table_info={
            "__tablename__": self.__table_name__,
            "id":Column(Integer, Sequence('{0}_id_seq'.format(
                self.__table_name__
            )), primary_key=True)
        }
        for f in field_names:
            field_info = cls.__dict__[f]
            col = None
            if field_info == str:
                col = Column(String)
            elif field_info == int:
                col = Column(Integer)
            elif field_info == bool:
                col = Column(Boolean)
            elif field_info == datetime:
                col = Column(DateTime)
            table_info.update({
                f: col
            })
        _model = type(self.__table_name__,(base,),table_info)
        ret = BaseEntity()
        ret.__model__ = _model
        return ret




def table(table_name):
    ret = __wrapper__(table_name)
    return ret.wrapper


class BaseEntity(object):

    def __init__(self):
        self.__model__ = None

    def __getitem__(self, item):
        if hasattr(self.__model__,item):
            return getattr(self.__model__,item)
        else:
            import sys
            if sys.version_info[0]==3:
                if self.__dict__.__contains__(item):
                    return self.__dict__[item]
                else:
                    raise(Exception("{0} was not found".format(item)))
            else:
                if self.__dict__.has_key(item):
                    return self.__dict__[item]
                else:
                    raise(Exception("{0} was not found".format(item)))







