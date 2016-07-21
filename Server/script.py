from flask import Blueprint, jsonify, request, make_response, current_app, send_from_directory
from flask.ext.restful import Api, Resource, reqparse
from lib.model import ScriptBase
import os

script_bp = Blueprint('script', __name__)
script_api = Api(script_bp)


class ScriptSet(object):

    def __init__(self):
        self._set = []
        self.update()

    def update(self):
        for s in os.listdir('scripts'):
            (name, ext) = os.path.splitext(s)
            if ext == '.py' and name != "__init__" and \
                name not in self.get_names():
                self._set.append(ScriptBase(name))

    def get_names(self):
        names = []
        for s in self._set:
            names.append(s.name)
        return names

    def __iter__(self):
        return iter(self._set)


class Script(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass


class ListScript(Resource):
    def get(self):
        script_set.update()
        result = []
        for s in script_set:
            result.append((s.name, s.is_enable))
        return result

class DownloadScript(Resource):
    def get(self, name):
        return send_from_directory('scripts', name + '.py')


script_set = ScriptSet()
script_api.add_resource(Script, '/script')
script_api.add_resource(ListScript, '/list/script')
script_api.add_resource(DownloadScript, '/download/script/<string:name>')
