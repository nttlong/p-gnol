def get_item(language,appname,view,key,value):
    from django.conf import settings
    from xdj import pymqr,medxdb
    if not hasattr(settings,"COLLECTION_LANGUAGE"):
        raise Exception("It looks like you forgot set 'COLLECTION_LANGUAGE' in django settings")
    qr = pymqr.query(medxdb.db(),settings.COLLECTION_LANGUAGE)
    if value == None:
        value =key
    value=value.lstrip(" ").rstrip(" ")
    key = key.lstrip(" ").rstrip(" ").lower()
    appname = appname.lower()
    view = view.lower()
    language = language.lower()
    x = qr.new().where([
        pymqr.filters.language == language,
        pymqr.filters.app == appname,
        pymqr.filters.view == view,
        pymqr.filters.key ==key
    ]).object
    if x.is_empty():
        qr.new().insert(
            language = language,
            app =appname,
            view =view,
            key = key,
            value = value
        ).commit()
        return value
    else:
        return x.value