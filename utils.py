from db import db

def get_all_records(cls):
    objs = db.session.execute(db.select(cls)).scalars()
    cols = cls.get_cols()
    resp = [{col: getattr(obj, col) for col in cols} for obj in objs]
    return resp

def insert_record(response, cls):
    obj = cls(response)
    db.session.add(obj)
    db.session.commit()