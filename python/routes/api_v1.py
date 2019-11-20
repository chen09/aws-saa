from flask import Blueprint
from flask_restful import Api
from resources import question, language, ppp, ccc

api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

api.add_resource(language.LanguageListResource, '/languages')
api.add_resource(language.LanguageResource, '/language/<string:id>')

api.add_resource(question.QuestionsListResource, '/questions')
api.add_resource(question.QuestionsCountResource, '/questions/count')
api.add_resource(question.QuestionsLanguagesResource, '/questions/languages')
api.add_resource(question.QuestionRandomResource, '/question/random/<string:language_id>')

api.add_resource(ppp.PppListResource, '/ppps')
api.add_resource(ppp.PppResource, '/ppp/<string:id>')
api.add_resource(ccc.CccListResource, '/cccs')
api.add_resource(ccc.CccResource, '/ccc/<string:id>')
