from flask import Blueprint, jsonify, make_response
from flask.ext.restful import Api, Resource, reqparse
from lib.filter import DuplicatedFlowFilter
from Server.script import script_set
from Server.db import client
from Server.auth import login_required
import json


METHOD = 'M'
URL = 'U'
FORM = 'F'
REFERER = 'R'
COOKIE = 'C'
OTHER = 'O'


def init_parse():

    parser = reqparse.RequestParser()
    parser.add_argument(METHOD, type=str)
    parser.add_argument(URL, type=str)
    parser.add_argument(FORM, type=str)
    parser.add_argument(REFERER, type=str)
    parser.add_argument(COOKIE, type=str)
    parser.add_argument(OTHER, type=str)
    parser.add_argument('action', type=str)
    return parser

flow_filter = DuplicatedFlowFilter()
parser = init_parse()
job_bp = Blueprint('job', __name__)
job_api = Api(job_bp)
job_db = client.centaur


class JobPool(object):
    """
    The Pool for celery.result.AsyncResult object.
    """
    def __init__(self, capacity=200):
        self._list = []
        self.capacity = capacity

    def __iter__(self):
        return iter(self._list)

    def __getitem__(self, index):
        return self._list[index]

    def add(self, job):
        if len(self._list) >= self.capacity:
            self._list.pop(0)
        self._list.append(job)


class Job(Resource):
    method_decorators = [login_required]

    def get(self, id):
        job = job_db.celery_taskmeta.find_one({'_id': id})
        if job:
            job['date_done'] = str(job['date_done'])
            job['result'] = json.loads(job['result'])
        return job

    def post(self, id):
        # forget, revoke,
        args = parser.parse_args()
        job = None
        for j in pool:
            if j.id == id:
                job = j
                break

        if args['action'] not in ('forget', 'revoke'):
            response = make_response(jsonify({
                "msg": "Invalid action."
            }), 400)
            return response

        if job:
            if args['action'] == 'forget':
                try:
                    job.forget()
                    return make_response("Success")
                except:
                    return make_response("Failed", 500)

            elif args['action'] == 'revoke':
                try:
                    job.revoke()
                    return make_response("Success")
                except:
                    return make_response("Failed", 500)

            else:
                response = make_response(jsonify({
                    "msg": "Invalid action."
                }), 400)
                return response
        else:
            response = make_response(jsonify({
                "msg": "Invalid job id or it is not in the pool."
            }), 400)
            return response


class AddJob(Resource):

    def put(self):
        flow = parser.parse_args()
        if flow not in flow_filter:
            for script in script_set:
                if script.invoke_check(flow):
                    job = script.send_task(flow=flow)
                    pool.add(job)
            flow_filter.add(flow)


class ListJob(Resource):

    method_decorators = [login_required]

    def get(self):
        result = []
        for s in pool:
            result.append((s.id, s.status, s.result))
        return result

pool = JobPool()
job_api.add_resource(AddJob, '/job')
job_api.add_resource(Job, '/job/<string:id>')
job_api.add_resource(ListJob, '/list/job')
