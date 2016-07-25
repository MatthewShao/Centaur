from flask import Blueprint, jsonify, request, make_response, current_app
from flask.ext.restful import Api, Resource, reqparse
from lib.filter import DuplicatedFlowFilter
from Server.script import script_set

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
    return parser

flow_filter = DuplicatedFlowFilter()
parser = init_parse()
job_bp = Blueprint('job', __name__)
job_api = Api(job_bp)


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
    # refer: https://github.com/celery/celery/blob/master/celery/backends/mongodb.py#L164

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        flow = parser.parse_args()
        if flow not in flow_filter:
            for script in script_set:
                if script.invoke_check(flow[URL]):
                    job = script.send_task(flow=flow)
                    pool.add(job)
            flow_filter.add(flow)


class ListJob(Resource):

    def get(self):
        pass

pool = JobPool()
job_api.add_resource(Job, '/job')
job_api.add_resource(ListJob, '/list/job')
