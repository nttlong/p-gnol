import xdj_sql as sql
from model.base import BaseHrModel
@sql.table(
    table_name="emps"
)
class Emps(BaseHrModel):

    Code = sql.fields.text(unique =True)
    FirstName = sql.fields.text(max_len=200, require = True)
    LastName = sql.fields.text(max_len=200, require = True)
    BirthDate = sql.fields.date(require=True)