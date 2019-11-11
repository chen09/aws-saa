from . import db
from .base import BaseModel


class ChoiceModel(db.Model, BaseModel):
    __tablename__ = 'choice'

    question_id = db.Column(db.Integer)
    language_id = db.Column(db.Integer)
    choice_id = db.Column(db.Integer)
    choice = db.Column(db.String)
