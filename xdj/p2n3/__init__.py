import sys
def has_key(obj,key):
    if isinstance(obj,dict):
        if sys.version_info[0] == 2:
            return obj.has_key(key)
        if sys.version_info[0] == 3:
            return obj.__contains__(key)
