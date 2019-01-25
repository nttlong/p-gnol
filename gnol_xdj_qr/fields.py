class __Fields__(object):
    def __getattr__(self, item):
        return __Field__(item)

Fields = __Fields__()


class __Field__(object):
    def __init__(self,name):
        self.__field_name__ = name
    def __eq__(self, other):
        from django.db.models import Q
