__engine__ = None
def get_engine():
    global  __engine__
    if not __engine__:
        from django.conf import settings
        from sqlalchemy import create_engine
        _engine = settings.DATABASES["default"]["ENGINE"]
        _user = settings.DATABASES["default"]["USER"]
        _password = settings.DATABASES["default"]["PASSWORD"]
        _host = settings.DATABASES["default"]["HOST"]
        _port = settings.DATABASES["default"]["PORT"]
        _name = settings.DATABASES["default"]["NAME"]

        if _engine == "django.db.backends.mysql":
            __engine__ = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(
                _user,
                _password,
                _host,
                _port,
                _name
            ))
        else:
            raise Exception("Can not create engine with {0}".format(_engine))
    return __engine__

class connect(object):
    def __init__(self):
        self.__session__ = None

    def __enter__(self):
        from sqlalchemy.orm import sessionmaker
        x = get_engine()
        Session = sessionmaker(bind=x)
        self.__session__ = Session()
        return self

    def open(self):
        from sqlalchemy.orm import sessionmaker
        x = get_engine()
        Session = sessionmaker(bind=x)
        self.__session__ = Session()

    def query(self,tbl):
        from .tables import BaseEntity
        from .queryable import __queryable__
        if isinstance(tbl,BaseEntity):
            return __queryable__(self.__session__,tbl)


    def __exit__(self, exc_type, exc_val, exc_tb):
        from sqlalchemy.orm.session import Session
        if isinstance(self.__session__,Session):
            self.__session__.close()

