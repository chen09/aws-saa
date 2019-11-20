from . import db
from .base import BaseModel


class LanguageModel(db.Model, BaseModel):
    __tablename__ = 'language'

    code = db.Column(db.String)
    source = db.Column(db.Boolean)
    target = db.Column(db.Boolean)

    # questions = db.relationship("QuestionModel", back_populates="language")
