app_name = "hr"
host_dir = "hr"
rel_login_url="login"


def on_authenticate(sender):
    return True


def on_get_language_resource_item(language,appname,view,key,value):
    return value