#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package này dùng để mở rộng open edx app (dạng micro app)
"""

__apps__={}
__register_apps__ = {}
__controllers__ = []
__pages__ = []
__build_cached__ = None
__controllert_url_build_cache__ = None

from . controllers import Model
from xdj import p2n3
import sys

def create(urls):
    """
    Tạp app
    :param name:
    :param host_dir:
    :return:
    """
    urlpatterns = ()
    global __build_cached__
    if __build_cached__ == None:
        __build_cached__ = {}

    from django.conf.urls import url
    import django
    replace_urls = []
    check_urls = []
    for item in __controllers__:

        if item.instance.replace_url:
            replace_urls.append(item.instance)
        if item.instance.check_url:
            check_urls.append(item.instance)

        if not __apps__.has_key(item.instance.app_name):
            import os
            try:
                if item.instance.app_dir != None:
                    server_static_path = os.sep.join([
                        item.instance.app_dir,"static"
                    ])
                    urlpatterns+=(
                        url(r'^' + item.instance.host_dir + '/static/(?P<path>.*)$', django.views.static.serve,
                            {'document_root': server_static_path, 'show_indexes': True}),
                    )
            except Exception as ex:
                raise ex
            __apps__.update({
                item.instance.app_name:item.instance.app_name
            })
        if not __build_cached__.has_key(item.instance.on_get.im_func.func_code.co_filename):
            if item.url=="":
                print (item.instance.on_get.im_func.func_code.co_filename)
                urlpatterns +=(
                    url(r"^"+item.instance.host_dir + "$", item.instance.__view_exec__),
                    url(r"^"+item.instance.host_dir + "/$", item.instance.__view_exec__)
                )
            else:
                urlpatterns += (
                    url(r"^"+item.instance.host_dir +"/"+item.url+"$", item.instance.__view_exec__),
                    url(r"^"+item.instance.host_dir +"/"+item.url+"/$", item.instance.__view_exec__)
                )
            for sub_page in item.instance.sub_pages:
                if item.url == "":
                    urlpatterns += (
                        url(r"^" + item.instance.host_dir+"/"+sub_page.url + "$", sub_page.exec_request_get),
                        url(r"^" + item.instance.host_dir +"/"+sub_page.url+ "/$", sub_page.exec_request_get)
                    )
                else:
                    urlpatterns += (
                        url(r"^" + item.instance.host_dir + "/" + item.url+"/"+sub_page.url + "$", sub_page.exec_request_get),
                        url(r"^" + item.instance.host_dir + "/" + item.url+"/"+sub_page.url + "/$", sub_page.exec_request_get)
                    )
            __build_cached__.update({
                item.instance.on_get.im_func.func_code.co_filename:item.instance.on_get
            })
        # urlpatterns += (
        #     url(r'config/self_paced', ConfigurationModelCurrentAPIView.as_view(model=SelfPacedConfiguration)),
        #     url(r'config/programs', ConfigurationModelCurrentAPIView.as_view(model=ProgramsApiConfig)),
        #     url(r'config/catalog', ConfigurationModelCurrentAPIView.as_view(model=CatalogIntegration)),
        #     url(r'config/forums', ConfigurationModelCurrentAPIView.as_view(model=ForumsConfig)),
        # )
    if isinstance(urls,tuple):
        urls += urlpatterns
    for item in replace_urls:
        class cls_replacer():
            def __init__(self,obj):
                self.obj=obj
            def exec_url(self,request,*args,**kwargs):
                return self.obj.__view_exec__(request,*args,**kwargs)
        print ("will replace with {0}".format(item.replace_url))
        match_url = [x for x in urls if x.regex.pattern == item.replace_url]
        if match_url.__len__() == 0:
            print ("{0} can not find replacer, will run under {1}".format(item.replace_url,item.url))
        else:
            import inspect
            print ("{0} can not find replacer, will run by controller {1} in {2}".format(match_url[0].regex.pattern , item,inspect.getfile(item.__class__)))
            x= cls_replacer(item)
            match_url[0].callback = x.exec_url
    for item in check_urls:
        print ("{0} will be check".format(item.check_url))
        match_url = [x for x in urls if x.regex.pattern == item.check_url]
        if match_url.__len__() == 0:
            print ("{0} can not find checker, will run under {1}".format(item.check_url,item.url))
        else:
            import inspect
            print ("{0} will be check by controller {1} in {2}".format(match_url[0].regex.pattern , item,inspect.getfile(item.__class__)))
            class obj_check_url():
                def __init__(self,obj,origin_callback):
                    self.obj = obj
                    self.__origin_callback__ = origin_callback
                def check_request(self,request,*args,**kwargs):
                    ret = self.obj.__view_exec__(request, *args, **kwargs)
                    if ret:
                        if issubclass(type(ret),Handler):
                            _ret = ret.OnBeforeHandler(ret.model)
                            if _ret==None:
                                _ret = self.__origin_callback__(request,*args,**kwargs)
                                ret.model.origin_result= _ret
                                _ret = ret.OnAfterHandler(ret.model)
                                if _ret == None:
                                    return ret.model.origin_result
                                else:
                                    return _ret
                        return ret
                    else:
                        return self.__origin_callback__(request, *args, **kwargs)

            x_obj = obj_check_url(item,match_url[0].callback)
            # item.__origin_callback__ = x_obj.check_request
            # def __check_request__(request,*args,**kwargs):
            #     ret = item.__view_exec__(request,*args,**kwargs)
            #     if ret:
            #         return ret
            #     else:
            #         return item.__origin_callback__(request,*args,**kwargs)


            match_url[0].callback = x_obj.check_request



    if isinstance(urls, list):
        urls.extend(list(urlpatterns))

    # x = [x for x in urls if x._regex == r"^static\/(?P<path>.*)$"]
    # u = x[0]
    # print x[0].default_args["document_root"]
    return urls
from . controllers import BaseController,Controller
from .page import Page

def register_INSTALLED_APPS(for_lms):
    from django.conf import settings
    # if settings.INSTALLED_APPS.count("xdj_models.models") == 0:
    #     settings.INSTALLED_APPS.append("xdj_models.models")
    try:
        load_moddels()
        load_settings(for_lms)
        load_config()

        load_email_settings()
        load_feature_settings()
        load_elastic_search_config()
        settings.MIDDLEWARE_CLASSES.append("xdj.middle_ware.GlobalRequestMiddleware")
    except Exception as ex:
        raise Exception(ex)

def load_apps(path_to_app_dir,urlpatterns=None,ignore_app_installed=False):
    if not ignore_app_installed:
        from django.conf import settings
        if settings.INSTALLED_APPS.count("xdj_models.models") == 0:
            raise Exception("it look like you forgot call xdj.register_INSTALLED_APPS() at manage.py , cms/bitnami_wsgi.py or lms/bitnami_wsgi.py before startup.run()\n"
                            "How to use xdj?\n"
                            "At before startup.run() for dev mode or for deploy mode bottom of '{edx source}/apps/edx/edx-platform/lms/envs/bitnami.py' put follow code:\n"
                            "import sys\n"
                            "sys.path.append(path to parent of xdj package)\n"
                            "import xdj"
                            "xdj.register_INSTALLED_APPS()\n"
                            "")

    if urlpatterns==None:
        urlpatterns=()
    import os
    import sys
    import imp
    import xdj
    global __controllert_url_build_cache__
    if __controllert_url_build_cache__ == None:
        __controllert_url_build_cache__ = {}
    sys.path.append(path_to_app_dir)
    apply_settings()
    def get_all_sub_dir():
        if sys.version_info[0] == 2:
            lst=[x for x in os.walk(path_to_app_dir).next()[1] if x.find(".")==-1]
            return lst
        if sys.version_info[0] == 3:
            lst = [x for x in os.walk(path_to_app_dir).__next__()[1] if x.find(".") == -1]
            return lst
    lst_sub_dirs = get_all_sub_dir()
    for item in lst_sub_dirs:
        full_path_to_app = os.sep.join([path_to_app_dir,item])
        sys.path.append(full_path_to_app)
        controller_dir = os.sep.join([path_to_app_dir,item,"controllers"])
        if not hasattr(xdj, "apps"):
            setattr(xdj, "apps", imp.new_module("xdj.apps"))
        if not hasattr(xdj.apps, item):
            setattr(xdj.apps, item, imp.new_module("xdj.apps.{0}".format(item)))
        app_settings = None
        try:
            app_settings = imp.load_source("xdj.apps.{0}.settings".format(item),os.sep.join([path_to_app_dir,item,"settings.py"]))
        except exceptions.IOError as ex:
            raise Exception("{0} was not found or error".format(
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        except Exception as ex:
            raise ex
        if not hasattr(app_settings,"app_name"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "app_name",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not hasattr(app_settings,"on_authenticate"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "on_authenticate",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not callable(app_settings.on_authenticate):
            raise Exception("{0} in {1} must be a function with one param".format(
                "on_authenticate",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not hasattr(app_settings,"host_dir"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "host_dir",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if sys.version_info[0] == 2:
            if not type(app_settings.host_dir) in [str,unicode]:
                raise Exception(
                    "{0} in {3} mut be in {1}, not is {2}".format(
                        "host_dir",
                        [str,unicode],
                        app_settings.host_dir,
                        os.sep.join([path_to_app_dir, item, "settings.py"])
                    )
                )
        if sys.version_info[0] == 3:
            if not type(app_settings.host_dir) in [str]:
                raise Exception(
                    "{0} in {3} mut be in {1}, not is {2}".format(
                        "host_dir",
                        [str],
                        app_settings.host_dir,
                        os.sep.join([path_to_app_dir, item, "settings.py"])
                    )
                )
        if not hasattr(app_settings,"on_get_language_resource_item"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "on_get_language_resource_item",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not callable(app_settings.on_get_language_resource_item):
            raise Exception("'{0}' in '{1}' must be a function like bellow\n"
                            "on_get_language_resource_item(language,appname,view,key,value)".format(
                "on_get_language_resource_item",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        if not hasattr(app_settings,"rel_login_url"):
            raise Exception("'{0}' was not found in '{1}'".format(
                "rel_login_url",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))
        import inspect
        if inspect.getargspec(app_settings.on_get_language_resource_item).args.__len__()<4:
            raise Exception("'{0}' in '{1}' must be a function like bellow\n"
                            "on_get_language_resource_item(language,appname,view,key,value)".format(
                "on_get_language_resource_item",
                os.sep.join([path_to_app_dir, item, "settings.py"])
            ))

        _app=getattr(xdj.apps, item)
        if not hasattr(_app,"settings"):
            setattr(_app,"settings",app_settings)

        sys.path.append(controller_dir)
        files = os.listdir(controller_dir)
        for file in files:

            import inspect
            controller_file = os.sep.join([controller_dir,file])
            extension = os.path.splitext(controller_file)[1][1:]
            if (not p2n3.has_key(__controllert_url_build_cache__,controller_file)) and extension=="py":
                m = None
                try:
                    m = imp.load_source("{0}.{1}".format(item,file.split('.')[0]),controller_file)
                except SyntaxError as ex:
                    raise ex
                except Exception as ex:
                    from xdj.errors import LoadControllerError
                    raise LoadControllerError(ex.message,file,ex.args)

                if __controllers__.__len__()>0:
                    controller_instance=__controllers__[__controllers__.__len__()-1].instance
                    class_file = inspect.getfile(controller_instance.__class__)
                    extension_class = os.path.splitext(class_file)[1][1:]
                    class_file = class_file[0:class_file.__len__() - extension_class.__len__()]
                    controller_file_class = controller_file[0:controller_file.__len__() - extension.__len__()]
                    if class_file == controller_file_class:
                        __controllers__[__controllers__.__len__() - 1].app_dir = os.sep.join([path_to_app_dir,item])
                        controller_instance.app_dir = os.sep.join([path_to_app_dir,item])
                        controller_instance.host_dir = app_settings.host_dir
                        controller_instance.app_name = app_settings.app_name
                        controller_instance.on_authenticate = app_settings.on_authenticate
                        controller_instance.rel_login_url = app_settings.rel_login_url
                        controller_instance.settings = app_settings
                        controller_instance.param_names = __controllers__[__controllers__.__len__()-1].params
                        print (controller_instance.url)
                        print (inspect.getfile(controller_instance.__class__))

                        from . controllers import Res
                        controller_instance.res = Res(app_settings.on_get_language_resource_item,controller_instance.app_name,controller_instance.template)
                    else:
                        print ("uncontroller file {0}".format(
                            controller_file
                        ))
                    __controllert_url_build_cache__.update({
                        controller_file:controller_instance
                    })

            """
            # self.controllerClass()
            if self.instance.app_name==None:
                raise Exception("{0} do not have 'app_name'".format(self.controllerClass))
            if self.instance.app_dir==None:
                raise Exception("{0} do not have 'app_dir'".format(self.controllerClass))
            """
            # x=1

    return create(urlpatterns)

class dobject(object):
    def __init__(self,*args,**kwargs):
        def feed_data(data):
            if isinstance(data,dobject):
                data =data.__dict__
            for k,v in data.items():
                    if isinstance(v,dict):
                        self.__dict__.update({
                            k:dobject(v)
                        })
                    elif isinstance(v,dobject):
                        self.__dict__.update({
                            k: v
                        })

                    elif isinstance(v,list):
                        lst =[]
                        for item in v:
                            lst.append(dobject(item))
                        self.__dict__.update({
                            k:lst
                        })
                    else:
                        self.__dict__.update({
                            k:v
                        })
        if args.__len__()==0:
            feed_data(kwargs)
        else:
            feed_data(args[0])

def apply_settings():
    """
    https://openedx.atlassian.net/wiki/spaces/AC/pages/34734726/edX+Feature+Flags
    :return:
    """
    from django.conf import settings
    setattr(settings,"USE_DJANGO_PIPELINE",True)
    """
    http://django-pipeline.readthedocs.org/ – whatever version we specify in our requirements.txt
    """
    setattr(settings,"DISPLAY_DEBUG_INFO_TO_STAFF",True)
    """For large courses this slows down courseware access for staff."""
    setattr(settings,"MILESTONES_APP",True)

def load_config():
    import json
    import os
    import sys
    filet_of_data_config = os.sep.join([os.path.dirname(__file__),"config","data.json"])
    with open( filet_of_data_config,'r') as data_file:
        from django.conf import settings
        data = json.loads(data_file.read())
        settings.DATABASES['default']['ENGINE'] = data["sql"]["engine"]
        settings.DATABASES['default']['NAME'] = data["sql"]["name"]
        settings.DATABASES['default']['PORT'] = data["sql"]["port"]
        settings.DATABASES['default']['HOST'] = data["sql"]["host"]
        settings.DATABASES['default']['USER'] = data["sql"]["user"]
        settings.DATABASES['default']['PASSWORD'] = data["sql"]["password"]

        settings.DATABASES["read_replica"]['ENGINE'] = data["sql"]["engine"]
        settings.DATABASES["read_replica"]['NAME'] = data["sql"]["name"]
        settings.DATABASES["read_replica"]['PORT'] = data["sql"]["port"]
        settings.DATABASES["read_replica"]['HOST'] = data["sql"]["host"]
        settings.DATABASES["read_replica"]['USER'] = data["sql"]["user"]
        settings.DATABASES["read_replica"]['PASSWORD'] = data["sql"]["password"]

        settings.DATABASES['student_module_history']['ENGINE'] = data["sql"]["engine"]
        settings.DATABASES['student_module_history']['NAME'] = data["sql"]["name"]
        settings.DATABASES['student_module_history']['PORT'] = data["sql"]["port"]
        settings.DATABASES['student_module_history']['HOST'] = data["sql"]["host"]
        settings.DATABASES['student_module_history']['USER'] = data["sql"]["user"]
        settings.DATABASES['student_module_history']['PASSWORD'] = data["sql"]["password"]

        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["db"] = data["mongo"]["name"]
        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["host"] = data["mongo"]["host"]
        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["user"] = data["mongo"]["user"]
        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["password"] = data["mongo"]["password"]
        settings.CONTENTSTORE["DOC_STORE_CONFIG"]["port"] = data["mongo"]["port"]

        settings.CONTENTSTORE["OPTIONS"]["db"] = data["mongo"]["name"]
        settings.CONTENTSTORE["OPTIONS"]["host"] = data["mongo"]["host"]
        settings.CONTENTSTORE["OPTIONS"]["user"] = data["mongo"]["user"]
        settings.CONTENTSTORE["OPTIONS"]["password"] = data["mongo"]["password"]
        settings.CONTENTSTORE["OPTIONS"]["port"] = data["mongo"]["port"]

        settings.DOC_STORE_CONFIG["db"] = data["mongo"]["name"]
        settings.DOC_STORE_CONFIG["host"] = data["mongo"]["host"]
        settings.DOC_STORE_CONFIG["user"] = data["mongo"]["user"]
        settings.DOC_STORE_CONFIG["password"] = data["mongo"]["password"]
        settings.DOC_STORE_CONFIG["port"] = data["mongo"]["port"]

        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["db"] = data["mongo"]["name"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["host"] = data["mongo"]["host"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["user"] = data["mongo"]["user"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["password"] = data["mongo"]["password"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][0]["DOC_STORE_CONFIG"]["port"] = data["mongo"]["port"]

        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["db"] = data["mongo"]["name"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["host"] = data["mongo"]["host"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["user"] = data["mongo"]["user"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["password"] = data["mongo"]["password"]
        settings.MODULESTORE["default"]["OPTIONS"]["stores"][1]["DOC_STORE_CONFIG"]["port"] = data["mongo"]["port"]

def load_settings(for_lms):
    from django.conf import settings
    import json
    import os
    import sys
    import logging
    logger = logging.getLogger(__name__)
    logger.info("load settings")

    filet_of_settings_config = os.sep.join([os.path.dirname(__file__), "config", "settings.json"])
    with open(filet_of_settings_config, 'r') as data_file:

        data = json.loads(data_file.read())
        logger.info(data)
        for k,v in data.items():
            setattr(settings,k,v)
        if data.has_key("MAKO_TEMPLATE_DIRS_BASE"):
            settings.TEMPLATES[0]['DIRS'] = data["MAKO_TEMPLATE_DIRS_BASE"]
            settings.TEMPLATES[1]['DIRS'] = data["MAKO_TEMPLATE_DIRS_BASE"]

    import path
    if data.has_key("STATIC_ROOT"):
        settings.STATIC_ROOT = path.path(data["STATIC_ROOT"])
        p = [x for x in settings.STATICFILES_DIRS if
             x.__str__()[x.__str__().__len__() - "/lms/static".__len__():] not in ["/lms/static", "/cms/static"]]
        # p.append(settings.STATIC_ROOT)
        settings.STATICFILES_DIRS = p
    if for_lms:
        if hasattr(settings,"LMS_TEMPLATE"):
            x = os.sep.join([settings.REPO_ROOT, "lms","templates"])
            settings.MAKO_TEMPLATE_DIRS_BASE = [p for p in settings.MAKO_TEMPLATE_DIRS_BASE if p.__str__() != x]
            settings.MAKO_TEMPLATE_DIRS_BASE.append(settings.LMS_TEMPLATE)
            settings.DEFAULT_TEMPLATE_ENGINE_DIRS=settings.MAKO_TEMPLATE_DIRS_BASE
            settings.TEMPLATES[0]['DIRS'] = settings.MAKO_TEMPLATE_DIRS_BASE
            settings.TEMPLATES[1]['DIRS'] = settings.MAKO_TEMPLATE_DIRS_BASE
    else:
        if hasattr(settings,"CMS_TEMPLATE"):
            x = os.sep.join([settings.REPO_ROOT, "cms", "templates"])
            settings.MAKO_TEMPLATE_DIRS_BASE = [p for p in settings.MAKO_TEMPLATE_DIRS_BASE if p.__str__() != x]
            settings.MAKO_TEMPLATE_DIRS_BASE.append(settings.CMS_TEMPLATE)
            settings.DEFAULT_TEMPLATE_ENGINE_DIRS=settings.MAKO_TEMPLATE_DIRS_BASE
            settings.TEMPLATES[0]['DIRS'] = settings.MAKO_TEMPLATE_DIRS_BASE
            settings.TEMPLATES[1]['DIRS'] = settings.MAKO_TEMPLATE_DIRS_BASE
    settings.WEBPACK_LOADER["DEFAULT"]["STATS_FILE"] = settings.WEBPACK_LOADER["DEFAULT"]["STATS_FILE"].replace(",/",
                                                                                                                "/")



    return  None

def load_email_settings():
    try:
        import json
        import os
        import sys
        filet_of_settings_config = os.sep.join([os.path.dirname(__file__), "config", "email.json"])
        with open(filet_of_settings_config, 'r') as data_file:
            from django.conf import settings
            data = json.loads(data_file.read())
            settings.EMAIL_HOST = data['host']
            settings.EMAIL_HOST_USER = data['user']
            settings.EMAIL_HOST_PASSWORD = data['password']
            settings.EMAIL_USE_TLS = data["tsl"]
            settings.EMAIL_PORT = data["port"]
            settings.EMAIL_FILE_PATH = data["path"]
            settings.SERVER_EMAIL = data["email"]
            settings.DEFAULT_FROM_EMAIL =data["email"]
            settings.CONTACT_EMAIL = data["contact_email"]
            settings.API_ACCESS_FROM_EMAIL = data["email"]
            settings.API_ACCESS_MANAGER_EMAIL = data["email"]
            settings.BUGS_EMAIL = data["email"]
            settings.BULK_EMAIL_DEFAULT_FROM_EMAIL = data["email"]
            settings.FEEDBACK_SUBMISSION_EMAIL =data["email"]
    except Exception as ex:
        from xdj.errors import LoadConfigError
        raise LoadConfigError(filet_of_settings_config,ex.message,ex)



def load_forum_config():
    import json
    import os
    import sys
    filet_of_settings_config = os.sep.join([os.path.dirname(__file__), "config", "forum.json"])
    with open(filet_of_settings_config, 'r') as data_file:
        from django.conf import settings
        data = json.loads(data_file.read())
        """
        "COMMENTS_SERVICE_KEY": "9198a36ca5349defcc6ecc1d3235390bd47a",
        "COMMENTS_SERVICE_URL": "http://localhost:18080"
        """
        settings.COMMENTS_SERVICE_KEY = data['key']
        settings.COMMENTS_SERVICE_URL = data['url']

def load_feature_settings():
    import json
    import os
    import sys
    filet_of_settings_config = os.sep.join([os.path.dirname(__file__), "config", "feature.json"])
    with open(filet_of_settings_config, 'r') as data_file:
        from django.conf import settings
        data = json.loads(data_file.read())
        for k,v in data.items():
            settings.FEATURES.update({
                k:v
            })

def load_moddels():
    import json
    import os
    filet_of_settings_config = os.sep.join([os.path.dirname(__file__), "config", "models.json"])
    with open(filet_of_settings_config, 'r') as data_file:
        from django.conf import settings
        data = json.loads(data_file.read())
        for item in data:
            if settings.INSTALLED_APPS.count(item) ==0:
                settings.INSTALLED_APPS.append(item)


def load_elastic_search_config():
    import json
    import os
    import sys
    filet_of_settings_config = os.sep.join([os.path.dirname(__file__), "config", "elastic_search.json"])
    with open(filet_of_settings_config, 'r') as data_file:
        from django.conf import settings
        data = json.loads(data_file.read())
        settings.ELASTIC_SEARCH_CONFIG=data

def debugTemplate(x):
    from xdj.middle_ware import GlobalRequestMiddleware
    request = GlobalRequestMiddleware.get_current_request()
    pass
def apply_context(context):
    def res(key,value=None):
        if value == None:
            value = key


        return value
    # context._data.update({"res": res})
    # context.res = res
    context.res = res
    # context._data["res"] = res
    # context["self"].context._data["res"] = res


class Handler(object):
    def from_json(self,txt):
        from xdj import JSON
        return JSON.from_json(txt)

    def __init__(self,model):
        self.model = model


def clear_language_cache():
    from xdj.controllers import clear_language_cache
    clear_language_cache()


def load_urls():
    from django.conf import settings
    import os
    settings.ROOT_URLCONF = []
    apps_dirs = os.sep.join([os.path.dirname(os.path.dirname(__file__)),"apps"])
    ret_url =  load_apps(apps_dirs,[],True)
    return ret_url






