from flask import Blueprint, jsonify, request, make_response, current_app, send_from_directory
from flask.ext.restful import Api, Resource, reqparse
from lib.model import ScriptBase
from werkzeug import FileStorage
from Server.auth import login_required
from mongoengine import DoesNotExist
import os
import re


def init_parse():
    parser = reqparse.RequestParser()
    parser.add_argument('file', type=FileStorage, location='files')
    parser.add_argument('action', type=str)
    parser.add_argument('invoke_rule', type=list, location='json')
    parser.add_argument('type', type=str)
    return parser

parser = init_parse()
script_bp = Blueprint('script', __name__)
script_api = Api(script_bp)


class ScriptSet(object):
    """
    The Set for ScriptBase object.
    """
    def __init__(self):
        self.pattern = re.compile('(?<=desc\s=\s""")[\s\S]*(?=""")')
        self._set = []
        self.update()

    def __iter__(self):
        return iter(self._set)

    def update(self):
        # regex: desc\s*=\s*"""[\s\S]*"""
        for s in os.listdir('scripts'):
            (name, ext) = os.path.splitext(s)
            if ext == '.py' and name != "__init__" and \
                name not in self.get_names():
                try:
                    # try to retrieve script from db
                    script = ScriptBase.objects(name=name).get()
                    self._set.append(script)
                except DoesNotExist:
                    # if not exist, parse the script file and store it in db
                    script_file = open('scripts/' + s, 'r')
                    text = script_file.read()
                    matchobj = self.pattern.search(text)
                    if matchobj:
                        desc = matchobj.group().strip()
                        script = ScriptBase(name=name, desc=desc, is_enable=True)
                        script.save()
                        self._set.append(script)

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
    method_decorators = [login_required]

    def post(self, name):
        args = parser.parse_args()
        script = script_set.get_script(name)
        if script:
            if args['action'] == 'toggle':
                return script.toggle_enable()

            elif args['action'] == 'set_rule':
                try:
                    script.set_invoke_rule(args['invoke_rule'])
                    return make_response("Success")
                except:
                    return make_response("Failed", 500)
            else:
                response = make_response(jsonify({
                    "msg": "Invalid action."
                }), 400)
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
            return make_response(jsonify({"msg": "Upload failed."}), 500)


class ListScript(Resource):
    method_decorators = [login_required]

    def get(self):
        script_set.update()
        result = []
        for s in script_set:
            script = {
                "name": s.name,
                "invoke_rule": s.rules,
                "is_enable": s.is_enable,
                "desc": s.desc
            }
            result.append(script)
        return jsonify(scripts=result)


class DownloadScript(Resource):

    def get(self, name):
        return send_from_directory('scripts', name + '.py')


script_set = ScriptSet()
script_api.add_resource(Script, '/script/<string:name>')
script_api.add_resource(ListScript, '/list/script')
script_api.add_resource(DownloadScript, '/download/script/<string:name>')
