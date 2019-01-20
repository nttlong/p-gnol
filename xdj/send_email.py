config = None
cache = None
COLLECTION_SETTINGS = "sys.email_settings"
COLLECTION_TEMPLATES = "sys.email_templates"
import threading
lock = threading.Lock()
def load_settings():
    from xdj import dobject
    from xdj import pymqr
    from xdj.medxdb import db
    from django.conf import settings
    global config
    if config == None:
        x = pymqr.query(db(),COLLECTION_SETTINGS).object
        if x.is_empty():
            v = pymqr.query(db(), COLLECTION_SETTINGS).insert(
                host="...",
                port=25,
                user="...",
                email="...",
                password="..."
            )
            v.commit()
            x = pymqr.query(db(), COLLECTION_SETTINGS).object
            config = dobject(
                host = x.host,
                port = x.port,
                user = x.user,
                password = x.password,
                email = x.email
            )
        else:
            config =x
def send_email(mail_to,subject,content):
    import smtplib, ssl
    load_settings()
    server = smtplib.SMTP(config.host, config.port)
    server.login(config.user, config.password)
    from email.mime.text import MIMEText as text
    m = text(content, 'html')
    m['Subject'] = subject
    m['Subject'] = 'Hello!'
    m['From'] = config.email
    m['To'] = mail_to
    return server.sendmail(config.email, mail_to,m.as_string())

def get_compile_template(language,name,defaultSubject,defaultTemplate,model):
    from xdj import dobject
    data = {}
    if isinstance(model,dobject) or isinstance(model,dict):
        if isinstance(model,dobject):
            data = model.__dict__
        else:
            data = model
        tmp = get_email_template(language,name,defaultSubject,defaultTemplate,model)

        from django.template import Context, Template
        t = Template(tmp["content"])
        c = Context(data)
        html = t.render(c)
        t_subject = Template(tmp["subject"])
        c_subject = Context(data)
        html_subject = t_subject.render(c_subject)
        return html_subject,html
    else:
        raise Exception("model must be 'xdj.dmobject' or 'dict'")

def send_email_by_template(mail_to,language,name,defaultSubject,defaultTemplate,model):
    subject , content =get_compile_template(language,name,defaultSubject,defaultTemplate,model)
    return send_email(mail_to,subject,content)

def unwind_model(model):
    from xdj import dobject
    ret = []
    if isinstance(model,dobject):
        return unwind_model(model.__dict__)
    if isinstance(model,dict):
        for k,v in model.items():
            if isinstance(v,dict):
                ret.extend([k+"."+x for x in unwind_model(v)])
            elif isinstance(v,dobject):
                ret.extend([k + "." + x for x in unwind_model(v.__dict__)])
            else:
                ret.append(k)
    return ret
def get_email_template(language,name,defaultSubject,defaultTemplate,model):
    global cache
    if cache == None:
        cache = {}
    if not cache.has_key(language):
        cache.update({
            language:{}
        })
    if cache[language].has_key(name):
        return cache[language][name]
    lock.acquire()
    try:


        import json
        from xdj import pymqr, medxdb
        from django.conf import settings
        import os
        if not hasattr(settings,"EMAIL_TEMPLATE_PATH"):
            raise Exception("It looks like you forgot put 'EMAIL_TEMPLATE_PATH' in settings of django")
        fields = unwind_model(model)
        qr = pymqr.query(medxdb.db(), COLLECTION_TEMPLATES)
        tmp = qr.new().where([pymqr.filters.language == language, pymqr.filters.name == name]).object
        if tmp.is_empty():
            language_dir = os.sep.join([settings.EMAIL_TEMPLATE_PATH, language])
            if not os.path.exists(language_dir):
                os.makedirs(language_dir)
            template_dir = os.sep.join([language_dir,name])
            if not os.path.exists(template_dir):
                os.makedirs(template_dir)
            model_file = os.sep.join([template_dir,"model.json"])
            if not os.path.exists(model_file):
                f_model = open(model_file,"w")
                f_model.write(json.dumps(fields))
                f_model.close()
            else:
                f_model = open(model_file,"r")
                txt = f_model.read()
                f_model.close()
                fields =json.loads(txt)

            tmp_file = os.sep.join([template_dir,"template.html"])
            if not os.path.exists(tmp_file):
                f_tmp = open(tmp_file,"w")
                f_tmp.write(defaultTemplate)
                f_tmp.close()
            else:
                f_tmp = open(tmp_file,"r")
                txt = f_tmp.read()
                defaultTemplate = txt

            tmp_subject = os.sep.join([template_dir,"subject.html"])
            if not os.path.exists(tmp_subject):
                f_tmp = open(tmp_subject,"w")
                f_tmp.write(defaultSubject)
                f_tmp.close()
            else:
                f_tmp = open(tmp_subject,"r")
                txt = f_tmp.read()
                defaultSubject = txt




            ret = qr.new().insert(
                language=language,
                name = name,
                template = defaultTemplate,
                subject= defaultSubject,
                fields = fields
            )
            ret.commit()
            cache[language].update({
                name:  {
                    "fields":fields,
                    "content":defaultTemplate,
                    "subject":defaultSubject
                }
            })
        else:
            cache[language].update({
                name: {
                    "fields": tmp.fields,
                    "content": tmp.template,
                    "subject":tmp.subject
                }
            })
        lock.release()
        return cache[language][name]
    except Exception as ex:
        lock.release()
        raise ex







