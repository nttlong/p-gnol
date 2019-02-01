from gnol.models.hr.deps import Depts
from xdj_sql import qr


def department_create(id,Code,Name, Username,parent_id):
    """
    Create or update dapartment
    :param id: if id ==0 try to create new department
    :param Code:
    :param Name:
    :param Username:
    :param parent_id:
    :return:
    """

    level = 1
    level_code = None
    if parent_id:
        parent = qr(Depts).where(Depts.id == parent_id).first()
        level = parent.Level + 1
        level_code = parent.LevelCode
    if qr(Depts).where(Depts.id == id).count() == 0:
        ret, error = qr(Depts).insert(
            Depts.Code >> Code,
            Depts.Name >> Name,
            Depts.CreatedBy >> Username,
            Depts.Level >> level,
            Depts.Parent_id >> parent_id
        )
        if error:
            return None, error
        if level_code:
            ret.LevelCode=level_code+"{0}.".format(ret.id)
        else:
            ret.LevelCode = ".{0}.".format(ret.id)
        ret.save()
        return ret, None
    else:
        ret =qr(Depts).where(Depts.id==id).update(
            Depts.Code >> Code,
            Depts.Name >> Name,
            Depts.ModifiedBy >> Username,
            Depts.Level >> level
        )
        return ret
