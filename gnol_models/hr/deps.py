import xdj_sql as sql
from gnol_models.hr.base import BaseHrModel,OrgBaseModel
@sql.table(table_name="depts")
class Depts(OrgBaseModel):
    pass

