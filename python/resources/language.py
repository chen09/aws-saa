import copy
import time

from flask import current_app, abort
from flask_restful import Resource, marshal_with, fields
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError

from app import hash_ids, HashidsEncode
from common import code, pretty_result
from models import db
from models.language import LanguageModel
from . import response_base_fields

language_fields = {
    # 'id': fields.Integer,
    'id': HashidsEncode(attribute='id'),
    'code': fields.String,
    'source': fields.Boolean,
    'target': fields.Boolean,
}

response_languages_fields = copy.copy(response_base_fields)
response_languages_fields['data'] = fields.Nested({'languages': fields.List(fields.Nested(language_fields))})


class LanguageListResource(Resource):

    def __init__(self):
        self.parser = RequestParser()

    @marshal_with(response_languages_fields)
    def get(self):
        start_time = time.time()
        self.parser.add_argument("id", type=str, location="args")
        self.parser.add_argument("code", type=str, location="args")

        args = self.parser.parse_args()

        try:
            languages = LanguageModel.query.filter(LanguageModel.useflg)
            if args.id is not None:
                languages = languages.filter(LanguageModel.id == hash_ids.decode(args.id))
            if args.code is not None:
                languages = languages.filter(LanguageModel.code.like('%' + args.code + '%'))
            languages = languages.all()

        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, 'DB Error!')
        else:
            return pretty_result(code.OK, start_time=start_time, data={'languages': languages})


response_language_fields = copy.copy(response_base_fields)
response_language_fields['data'] = fields.Nested({'language': fields.Nested(language_fields)})


class LanguageResource(Resource):
    def __init__(self):
        self.parser = RequestParser()

    @staticmethod
    @marshal_with(response_language_fields)
    def get(id):
        start_time = time.time()
        id = hash_ids.decode(id)
        if not id: abort(404)

        try:
            language = LanguageModel.query.filter(LanguageModel.id == id, LanguageModel.useflg).one()
            if not language: abort(404)
        except SQLAlchemyError as e:
            current_app.logger.error(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR, 'DB Error!')
        else:
            return pretty_result(code.OK, start_time=start_time, data={'language': language})
