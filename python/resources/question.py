from flask import current_app, abort
from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func

from app import hash_ids, HashidsEncode
from models import db
from common import code, pretty_result
from models.choice import ChoiceModel
from models.question import QuestionModel
from models.language import LanguageModel
import time

from . import response_base_fields
import copy

language_fields = {
    'id': HashidsEncode(attribute='id'),
    'code': fields.String,
}


class QuestionsCountResource(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        start_time = time.time()
        '''17 is en'''
        language_id = 17
        count = QuestionModel.query.filter(QuestionModel.language_id == language_id).count()

        data = {
            'questions': {
                'count': count
            }
        }
        return pretty_result(code.OK, data=data, start_time=start_time)


response_languages_fields = copy.copy(response_base_fields)
response_languages_fields['data'] = fields.Nested(
    {'questions': fields.Nested({'languages': fields.List(fields.Nested(language_fields))})})


class QuestionsLanguagesResource(Resource):
    def __init__(self):
        self.parser = RequestParser()

    @marshal_with(response_languages_fields)
    def get(self):
        start_time = time.time()
        try:
            languages = LanguageModel.query. \
                distinct(LanguageModel.id). \
                join(QuestionModel, LanguageModel.id == QuestionModel.language_id). \
                filter(LanguageModel.useflg). \
                filter(QuestionModel.useflg)

        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, 'DB Error!')
        else:
            return pretty_result(code.OK, start_time=start_time, data={'questions': {'languages': languages}})


language_fields = {
    'code': fields.String,
}

choice_fields = {
    'choice_id': fields.Integer,
    'choice': fields.String,
}

question_fields = {
    # 'id': HashidsEncode(attribute='id'),
    'question_id': HashidsEncode(attribute='question_id'),
    'language_id': HashidsEncode(attribute='language_id'),
    'question': fields.String,
    'remarks': fields.String,
    'language': fields.Nested(language_fields),
    'choices': fields.List(fields.Nested(choice_fields)),
}

response_questions_fields = copy.copy(response_base_fields)
response_questions_fields['data'] = fields.Nested({'questions': fields.List(fields.Nested(question_fields))})


class QuestionsListResource(Resource):

    def __init__(self):
        self.parser = RequestParser()

    @marshal_with(response_questions_fields)
    def get(self):
        start_time = time.time()
        self.parser.add_argument("offset", type=int, location="args", default=0)
        self.parser.add_argument("limit", type=int, location="args", default=10)

        '''9erj4rd8 17 en'''
        '''mnonxz3g 102 zh-CN'''
        self.parser.add_argument("language_id", type=str, location="args", default='9erj4rd8')

        args = self.parser.parse_args()
        if args.limit >= 50:
            return pretty_result(code.DB_ERROR, 'limit > 50')

        language_id = hash_ids.decode(args.language_id)

        try:
            questions = QuestionModel.query. \
                join(ChoiceModel,
                     ChoiceModel.language_id == QuestionModel.language_id \
                     and ChoiceModel.question_id == QuestionModel.question_id \
                     and ChoiceModel.useflg). \
                filter(QuestionModel.useflg). \
                filter(QuestionModel.language_id == language_id). \
                limit(args.limit).offset(args.offset).all()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.PARAM_ERROR, 'DB Error!', start_time=start_time)
        else:
            return pretty_result(code.OK, start_time=start_time, data={'questions': questions})


language_fields = {
    'code': fields.String,
}

question_fields = {
    # 'id': HashidsEncode(attribute='id'),
    'question_id': HashidsEncode(attribute='question_id'),
    'language_id': HashidsEncode(attribute='language_id'),
    'question': fields.String,
    'remarks': fields.String,
    'language': fields.Nested(language_fields),
}

response_question_fields = copy.copy(response_base_fields)
response_question_fields['data'] = fields.Nested({'question': fields.Nested(question_fields)})


class QuestionResource(Resource):

    @staticmethod
    @marshal_with(response_question_fields)
    def get(language_id, question_id):
        start_time = time.time()
        language_id = hash_ids.decode(language_id)
        question_id = hash_ids.decode(question_id)

        if not language_id: abort(404)
        if not question_id: abort(404)

        try:
            question = QuestionModel.query.filter(QuestionModel.language_id == language_id). \
                filter(QuestionModel.question_id == question_id). \
                one()
            print(question)
            if not question: abort(404)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, 'DB Error!')
        else:
            return pretty_result(code.OK, start_time=start_time, data={'question': question})


response_question2_fields = copy.copy(response_base_fields)
response_question2_fields['data'] = fields.Nested({'question': fields.Nested(question_fields)})


class QuestionRandomResource(Resource):

    @staticmethod
    @marshal_with(response_question2_fields)
    def get(language_id):
        start_time = time.time()
        language_id = hash_ids.decode(language_id)

        if not language_id: abort(404)

        try:
            question = QuestionModel.query.filter(QuestionModel.language_id == language_id). \
                order_by(func.rand()).limit(1).one()
            print(question)
            if not question: abort(404)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, 'DB Error!')
        else:
            return pretty_result(code.OK, start_time=start_time, data={'question': question})
