from flask import Blueprint, jsonify, request, make_response, current_app
from flask.ext.restful import Api, Resource, reqparse
from lib.model import ScriptBase

script_bp = Blueprint('script', __name__)
script_api = Api(script_bp)


class Script(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class ScriptList(Resource):
    def get(self):
        pass

script_api.add_resource(Script, '/job')
script_api.add_resource(ScriptList, '/list/job')
