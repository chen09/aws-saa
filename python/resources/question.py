import copy
import time

from flask import current_app, abort
from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func

from app import hash_ids_choice, hash_ids_language, hash_ids_question, HashidsEncode

from common import code, pretty_result
from models import db
from models.language import LanguageModel
from models.question import QuestionModel
from . import response_base_fields
from distutils.util import strtobool

language_fields = {
    'id': HashidsEncode(attribute='id', hash_ids=hash_ids_language),
    'code': fields.String,
}


class QuestionsCountResource(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        start_time = time.time()
        self.parser.add_argument("language_id", type=str, location="args", default='g51851on')
        args = self.parser.parse_args()
        '''17 is en'''
        language_id = hash_ids_language.decode(args.language_id)
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
    'choice_id': HashidsEncode(attribute='choice_id', hash_ids=hash_ids_choice),
    'choice': fields.String,
    # 'useflg': fields.Boolean
}

answer_fields = {
    'choice_id': HashidsEncode(attribute='choice_id', hash_ids=hash_ids_choice),
}

question_fields = {
    # 'id': HashidsEncode(attribute='id'),
    'question_id': HashidsEncode(attribute='id', hash_ids=hash_ids_question),
    'language_id': HashidsEncode(attribute='id', hash_ids=hash_ids_language),
    'question': fields.String,
    'remarks': fields.String,
    'language': fields.Nested(language_fields),
    'choices': fields.List(fields.Nested(choice_fields)),
    'answers': fields.List(fields.Nested(answer_fields)),
}

response_questions_fields = copy.copy(response_base_fields)
response_questions_fields['data'] = fields.Nested({'questions': fields.List(fields.Nested(question_fields))})


class QuestionsListResource(Resource):

    def __init__(self, request_parser=RequestParser()):
        self.parser = request_parser

    @marshal_with(response_questions_fields)
    def get(self):
        start_time = time.time()
        self.parser.add_argument("offset", type=int, location="args", default=0)
        self.parser.add_argument("limit", type=int, location="args", default=1)
        self.parser.add_argument("random", type=strtobool, location="args", default=True)

        '''g51851on 17 en'''
        '''dm1qgqky 102 zh-CN'''
        self.parser.add_argument("language_id", type=str, location="args", default='g51851on')

        args = self.parser.parse_args()
        if args.limit >= 50:
            return pretty_result(code.DB_ERROR, 'limit > 50')

        language_id = hash_ids_language.decode(args.language_id)

        # print(args.random)
        try:
            questions_filter = QuestionModel.query. \
                filter(QuestionModel.language_id == language_id). \
                filter(QuestionModel.useflg)
            if args.random:
                questions_filter = questions_filter.order_by(func.rand())

            questions = questions_filter. \
                limit(args.limit). \
                offset(args.offset). \
                all()
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.PARAM_ERROR, 'DB Error!', start_time=start_time)
        else:
            return pretty_result(code.OK, start_time=start_time, data={'questions': questions})
