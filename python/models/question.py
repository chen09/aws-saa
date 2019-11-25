from . import db
from .base import BaseModel

# from .language import LanguageModel
from .choice import ChoiceModel
from .answer import AnswerModel


class QuestionModel(db.Model, BaseModel):
    __tablename__ = 'question'

    question_id = db.Column(db.Integer)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    question = db.Column(db.String)
    remarks = db.Column(db.String)
    # language = db.relationship("LanguageModel", back_populates="questions")
    language = db.relationship("LanguageModel")

    # choices = db.relationship("ChoiceModel", foreign_keys=[question_id, language_id], primaryjoin=)
    choices = db.relationship(ChoiceModel, foreign_keys=[question_id, language_id], uselist=True,
                              order_by="ChoiceModel.choice_id",
                              primaryjoin="QuestionModel.question_id==ChoiceModel.question_id and"
                                          " QuestionModel.language_id==ChoiceModel.language_id")

    answers = db.relationship(AnswerModel, foreign_keys=[question_id], uselist=True,
                              order_by="AnswerModel.choice_id",
                              primaryjoin="QuestionModel.question_id==AnswerModel.question_id")

    # choices = relationship
    # choices = db.relationship(
    #     'ChoiceModel',
    #     secondary=ChoiceModel.__tablename__,
    #     back_populates=__tablename__,
    # )
