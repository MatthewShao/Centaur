from flask import Blueprint, jsonify, request, make_response, current_app, send_from_directory
from flask.ext.restful import Api, Resource, reqparse
from lib.model import ScriptBase
from werkzeug import FileStorage
import os


def init_parse():
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=FileStorage, location='files')
    parser.add_argument('action', type=str)
    parser.add_argument('invoke_rule', type=str)
    return parser

parser = init_parse()
script_bp = Blueprint('script', __name__)
script_api = Api(script_bp)


class ScriptSet(object):
    """
    The Set for ScriptBase object.
    """
    def __init__(self):
        self._set = []
        self.update()

    def __iter__(self):
        return iter(self._set)

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

    def get_script(self, name):
        script = None
        for s in self._set:
            if s.name == name:
                script = s
                break
        return script


class Script(Resource):

    def get(self, name):
        script = script_set.get_script(name)
        if script:
            try:
                f = open("scripts/" + script.name +".py", 'r')
                script_content = f.read()
                return jsonify({
                    "name" : script.name,
                    "invoke_rule" : script.invoke_rule,
                    "content": script_content,
                    "is_enable": script.is_enable
                })

            except IOError:
                response = make_response(jsonify({
                     "msg": "Fail to read script file."
                }))
                response.status_code = 500
                return response
        else:
            return None

    def post(self, name):
        args = parser.parse_args()
        script = script_set.get_script(name)
        if script:
            if args['action'] == 'toggle':
                return script.toggle_enable()
            if args['action'] == 'set_rule':
                try:
                    script.set_invoke_rule(args['invoke_rule'])
                    return make_response("Success")
                except:
                    return make_response("Failed")
            else:
                response = make_response(jsonify({
                    "msg": "Invalid action."
                }))
                response.status_code = 400
                return response

        else:
            return None

    def put(self, name):
        args = parser.parse_args()
        file = args['file']
        try:
            file.save('scripts/'+ name + '.py')
            script_set.update()
            return make_response(jsonify({"msg": name + ".py uploaded."}))

        except Exception:
            script_set.update()
            return make_response(jsonify({"msg": "Upload failed."}))


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
script_api.add_resource(Script, '/script/<string:name>')
script_api.add_resource(ListScript, '/list/script')
script_api.add_resource(DownloadScript, '/download/script/<string:name>')
