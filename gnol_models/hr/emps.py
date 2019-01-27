import xdj_sql as sql
from gnol_models.hr.base import BaseHrModel
from django.db import models
@sql.table(
    table_name="emps"
)
class Emps(BaseHrModel):

    Code = sql.fields.text(unique =True, require = True)
    FirstName = sql.fields.text(max_len=200, require = True)
    LastName = sql.fields.text(max_len=200, require = True)
    BirthDate = sql.fields.date(require=True)
    DeptId = sql.fields.integer()
    # Depts = sql.fields models.ForeignKey(to=Depts.__model__,to_field="id",db_column="DeptId")
    @sql.fields.lookup(
        local_fields= "DeptId",
        foreign_fields = "id"
    )
    def Dept(self):
        from gnol_models.hr.deps import Depts as D
        return D


fx=Emps.Dept().Code

x=fx






