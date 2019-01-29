import sys


def has_key(obj,key):
    if isinstance(obj,dict):
        if sys.version_info[0] == 2:
            return obj.has_key(key)
        if sys.version_info[0] == 3:
            return obj.__contains__(key)


def create_static(item,server_static_path):
    if sys.version_info[0] == 2:
        from django.conf.urls import url
        from django.conf.urls.static import static
        import django
        if item.instance.host_dir == "":
            return tuple(static('/static/', document_root=server_static_path))
        return tuple(static(item.instance.host_dir + '/static/(?P<path>.*)$', document_root=server_static_path))

    if sys.version_info[0] == 3:
        from django.conf.urls import url
        from django.conf.urls.static import static
        import django
        if item.instance.host_dir=="":
            return tuple(static('/static/', document_root=server_static_path))
        return tuple(static(item.instance.host_dir + '/static/(?P<path>.*)$', document_root=server_static_path))


def get_function_code_path(fn):
    if sys.version_info[0] == 2:
        return fn.im_func.func_code.co_filename
    else:
        return fn.__func__.__code__.co_filename


def get_url(item,fn):
    from django.conf.urls import url
    # if sys.version_info[0] == 2:
    if hasattr(item,"instance"):
        if item.url == "":
            if item.instance.host_dir=="":
                ret = (
                    url(r"^" + item.instance.host_dir + "$", fn)
                )
            else:
                ret = (
                    url(r"^" + item.instance.host_dir + "$", fn),
                    url(r"^" + item.instance.host_dir + "/$", fn)
                    )
            return ret
        else:
            if item.instance.host_dir == "":
                ret = (
                    url(r"^" + item.url + "$", fn),
                    url(r"^" + item.url + "/$", fn)
                )
                return ret
            else:
                ret= (
                    url(r"^" + item.instance.host_dir + "/" + item.url + "$", fn),
                    url(r"^" + item.instance.host_dir + "/" + item.url + "/$", fn)
                    )
                return ret
    else:
        if item.owner.host_dir == "":
            if item.url == "":
                ret = (
                    url(r"^" + item.owner.host_dir + "$", fn),
                    url(r"^" + item.owner.host_dir + "/$", fn)
                    )
                return ret
            else:
                ret= (
                    url(r"^"+ item.url+"$", fn),
                    url(r"^"+ item.url+"/$", fn)
                    )
                return ret
        else:
            if item.url == "":
                ret = (
                    url(r"^" + item.owner.host_dir + "$", fn),
                    url(r"^" + item.owner.host_dir + "/$", fn)
                    )
                return ret
            else:
                ret= (
                    url(r"^"+item.owner.host_dir + "/" + item.url+"$", fn),
                    url(r"^"+item.owner.host_dir + "/" + item.url+"/$", fn)
                    )
                return ret
    # else:
    #     if hasattr(item, "instance"):
    #         if item.url == "":
    #             ret = (
    #                 url(item.instance.host_dir + "$", fn),
    #                 )
    #             return ret
    #         else:
    #             ret= (
    #                 url(item.instance.host_dir + "/" + item.url+"$", fn),
    #                 url(item.instance.host_dir + "/" + item.url+"/$", fn)
    #                 )
    #             return ret
    #     else:
    #         if item.url == "":
    #             ret = (
    #                 url(r"^" + item.owner.host_dir + "$", fn),
    #                 url(r"^" + item.owner.host_dir + "/$", fn)
    #                 )
    #             return ret
    #         else:
    #             ret= (
    #                 url(r"^"+item.owner.host_dir + "/" + item.url+"$", fn),
    #                 url(r"^"+item.owner.host_dir + "/" + item.url+"/$", fn)
    #                 )
    #             return ret


