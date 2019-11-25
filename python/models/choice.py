from . import db
from .base import BaseModel


class ChoiceModel(db.Model, BaseModel):
    __tablename__ = 'choice'

    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'))
    language_id = db.Column(db.Integer, db.ForeignKey('question.language_id'))
    choice_id = db.Column(db.Integer)
    choice = db.Column(db.String)

