# import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()
from django.contrib.auth.models import User

from gnol_models.hr.deps import Depts
import test_001

x=User()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
from django.core.management import execute_from_command_line
# import django
# # import xdj
# # xdj.start()
# django.setup()

# execute_from_command_line(sys.argv)