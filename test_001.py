from xdj_sql import qr,Fields
from gnol_models.hr.emps import Emps
from gnol_models.hr.deps import Depts

x = qr(Emps)
x.select_related(Emps.Dept()).select(
    Emps.Dept().Code
)
v=x.all()
print (v)
