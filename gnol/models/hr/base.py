import xdj_sql as sql
from datetime import datetime
from django.db import models


class BaseHrModel():
    # Created by: The username
    CreatedBy = sql.fields.text(require=True)
    CreatedOn = sql.fields.text(require=True,default_value=datetime.utcnow())
    ModifiedBy = sql.fields.text()
    ModifiedOn = sql.fields.date()


class BaseCategories(BaseHrModel):
    Code = sql.fields.text(require=True, unique= True)
    Name = sql.fields.text(require=True)
    Description = sql.fields.text()


class OrgBaseModel(BaseCategories):

    Parent = models.ForeignKey('self',on_delete=None)
    Level = sql.fields.integer()
    LevelCode = sql.fields.text()



