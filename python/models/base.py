import datetime
from . import db


class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    useflg = db.Column(db.BOOLEAN, default=True)
    created = db.Column(db.DATETIME(), default=datetime.datetime.now)
    updated = db.Column(db.DATETIME(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
