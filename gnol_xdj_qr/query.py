class QR(object):
    def __init__(self,model):
        self.__model__ = model
        self.__selected_fields__ = {}

    def select(self,*args,**kwargs):
        from django.db.models.query_utils import DeferredAttribute
        if args.__len__()>0:
            for x in args:
                if isinstance(x,DeferredAttribute):
                    self.__selected_fields__.update({
                        x.field_name:1
                    })
                if type(x) in [str,unicode]:
                    self.__selected_fields__.update({
                        x:1
                    })
        return self

    def where(self,*args,**kwargs):
        return self

