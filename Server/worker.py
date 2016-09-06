from flask import Blueprint, make_response, jsonify
from flask.ext.restful import Api, Resource, reqparse
from Server.lib.celery_ import celery

def init_parse():
    parser = reqparse.RequestParser()
    parser.add_argument("task", type=str)
    return parser

worker_bp = Blueprint('worker', __name__)
worker_api = Api(worker_bp)
parser = init_parse()


class WorkerList(Resource):

    def get(self):
        inspect = celery.control.inspect()
        return jsonify(inspect.registered())


class Worker(Resource):

    def get(self, name):
        args = parser.parse_args()
        # select worker
        if name == 'all':
            inspect = celery.control.inspect()
        else:
            inspect = celery.control.inspect([name])
        # test if worker registered
        if inspect.registered():
            # if not specify the task, return the stats of the worker
            if args['task']:
                if args['task'] == 'active':
                    return jsonify(inspect.active())
                elif args['task'] == 'scheduled':
                    return jsonify(inspect.scheduled())
                elif args['task'] == 'reserved':
                    return jsonify(inspect.reserved())
                else:
                    response = make_response(jsonify({
                        "msg": "Invalid task type."
                    }))
                    response.status_code = 400
            else:
                response = jsonify(inspect.stats())
        else:
            response = make_response(jsonify({
                "msg": "Invalid worker name."
            }))
            response.status_code = 400
        return response

    def post(self, name):
        # TODO provide remote control operations, including
        # cancel consumers, pool restart, shutdown, purge
        pass


worker_api.add_resource(WorkerList, "/list/workers")
worker_api.add_resource(Worker, "/worker/<string:name>")
