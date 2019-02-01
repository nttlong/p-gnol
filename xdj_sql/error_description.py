from django.db.utils import IntegrityError


class BaseError(Exception):
    def __init__(self,message):
        super(BaseError,self).__init__(message)

class UniqueError(BaseError):
    def __init__(self, message, code, unique_name, fields):
        super(UniqueError,self).__init__(message)
        self.code = code
        self.unique_name = unique_name
        self.fields = fields

def mysql_get_unique_fields_by_unique_name(table_name,unique_name):
    from django.db import connections
    from django.conf import settings
    database = settings.DATABASES["default"]["NAME"]
    db_conn = connections['default']
    cursor = db_conn.cursor()
    cursor.execute(
        "select COLUMN_NAME "
        "from information_schema.KEY_COLUMN_USAGE "
        "where information_schema.KEY_COLUMN_USAGE.TABLE_SCHEMA='{0}' and "
        "information_schema.KEY_COLUMN_USAGE.CONSTRAINT_NAME='{1}' and "
        "information_schema.KEY_COLUMN_USAGE.TABLE_NAME ='{2}'".format(
            database,
            unique_name,
            table_name
            )
    )
    rows = cursor.fetchall()
    ret =[]
    for x in rows:
        for y in x:
            ret.append(y)

    return ret


def get_error(table_name,ex):
    from django.conf import settings
    if settings.DATABASES["default"]["ENGINE"]=="django.db.backends.mysql":
        if isinstance(ex,IntegrityError):
            if ex.args[0] == 1062:
                unique_name = ex.args[1].split("'")[3]
                fields = mysql_get_unique_fields_by_unique_name(table_name,unique_name)
                return UniqueError(
                    ex.args[1],
                    1062,
                    unique_name,
                    fields
                )
    else:
        raise Exception("Can not handle error with {0}".format(
            settings.DATABASES["default"]["ENGINE"]
        ))