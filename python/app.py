# -*- coding: utf-8 -*-
import string
import flask_restful
from flask import Flask, abort, jsonify
from hashids import Hashids
from models import db
from common import code, pretty_result
from flask_restful import fields
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

hash_ids = Hashids(salt='2c4w6ag2rtqemd3e', min_length=8, alphabet=string.ascii_lowercase + string.digits)

handle_exception = app.handle_exception
handle_user_exception = app.handle_user_exception


class HashidsEncode(fields.Raw):
    def format(self, value):
        return hash_ids.encode(value)


def _custom_abort(http_status_code, **kwargs):
    if http_status_code == 400:
        message = kwargs.get('message')
        if isinstance(message, dict):
            param, info = list(message.items())[0]
            data = '{}:{}!'.format(param, info)
            return abort(jsonify(pretty_result(code.PARAM_ERROR, data=data)))
        else:
            return abort(jsonify(pretty_result(code.PARAM_ERROR, data=message)))
    return abort(http_status_code)


def _access_control(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,PUT,PATCH,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = 86400
    return response


def create_app(config):
    app.config.from_object(config)
    app.after_request(_access_control)
    flask_restful.abort = _custom_abort
    db.init_app(app)
    from routes import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    app.handle_exception = handle_exception
    app.handle_user_exception = handle_user_exception
    return app
