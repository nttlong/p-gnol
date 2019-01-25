import xdj_sql as sql
class BaseHrModel():
    CreatedBy = sql.fields.text(require=True)
    CreatedOn = sql.fields.text(require=True)

