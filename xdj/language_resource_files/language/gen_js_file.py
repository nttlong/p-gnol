import polib
import json
import os
po = polib.pofile(os.getcwd()+os.sep+"/lv-packages/language/djangojs.po")
data={}
for entry in po:
    data.update({
        entry.msgid:entry.msgstr
    })
_data=json.dumps(data)

with open(os.getcwd()+os.sep+'/lv-packages/language/djangojs.js', 'w') as file:
    file.write(_data)
    # print entry.msgid, entry.msgstr