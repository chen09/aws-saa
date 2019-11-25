from . import db
from .base import BaseModel


class AnswerModel(db.Model, BaseModel):
    __tablename__ = 'answer'

    question_id = db.Column(db.Integer)
    choice_id = db.Column(db.Integer)
