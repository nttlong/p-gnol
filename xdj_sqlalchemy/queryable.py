

class __queryable__(object):

    def __init__(self,session,entity):
        self.__sesssion__ = session
        self.__entity__ = entity

    def where(self,*args,**kwargs):
        pass