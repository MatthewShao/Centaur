from flask import Blueprint, jsonify, request, make_response, current_app
from flask.ext.restful import Api, Resource, reqparse
from lib.filter import DuplicatedFlowFilter

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


class Job(Resource):

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        flow = parser.parse_args()
        if flow not in flow_filter:
            print flow
            flow_filter.add(flow)


class JobList(Resource):

    def get(self):
        pass

job_api.add_resource(Job, '/job')
job_api.add_resource(JobList, '/list/job')
