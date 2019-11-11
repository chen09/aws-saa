from . import db
from .base import BaseModel

from sqlalchemy.orm import relationship
from .choice import ChoiceModel


class QuestionModel(db.Model, BaseModel):
    __tablename__ = 'question'

    question_id = db.Column(db.Integer)
    language_id = db.Column(db.Integer)
    question = db.Column(db.String)
    remarks = db.Column(db.String)

    # choices = relationship("ChoiceModel")
    # choices = db.relationship(
    #     'ChoiceModel',
    #     secondary=ChoiceModel.__tablename__,
    #     back_populates=__tablename__,
    # )