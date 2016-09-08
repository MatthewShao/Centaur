from flask import Blueprint, make_response, jsonify
from flask.ext.restful import Api, Resource, reqparse
from Server.lib.celery_ import celery

def init_parse():
    parser = reqparse.RequestParser()
    parser.add_argument('task', type=str)
    parser.add_argument('action', type=str, location='json')
    parser.add_argument('dest', type=list, location='json')
    return parser

worker_bp = Blueprint('worker', __name__)
worker_api = Api(worker_bp)
parser = init_parse()


class WorkerList(Resource):

    def get(self):
        inspect = celery.control.inspect()
        return jsonify(inspect.registered())


class InspectWorker(Resource):

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
                    }), 400)
            else:
                response = jsonify(inspect.stats())
        else:
            response = make_response(jsonify({
                "msg": "Invalid worker name."
            }), 400)
        return response

class ManageWorker(Resource):

    def post(self):
        args = parser.parse_args()
        dest = args['dest']
        # check if dest worker registered
        if args['action'] == 'purge':
            count = celery.control.purge()
            return jsonify({"msg": "{} tasks have been discarded".format(count)})

        registered = celery.control.inspect(dest).registered()
        if not registered:
            response = make_response(jsonify({
                "msg": "Invalid woker name appears."
            }), 400)
            return response

        if args['action'] == 'cancel_consumer':
            return celery.control.cancel_consumer(args['task'], reply=True, destination=args['dest'])
        elif args['action'] == 'pool_restart':
            return celery.control.broadcast('pool_restart', arguments={'reload': True}, reply=True)
        elif args['action'] == 'shutdown':
            celery.control.broadcast('shutdown', destination=args['dest'])
            return jsonify({
                "msg": "Shutdown messages have sent to {}".args['dest']
            })
        else:
            response = make_response(jsonify({
                "msg": "Invalid action."
            }), 400)
            return response

worker_api.add_resource(WorkerList, "/list/workers")
worker_api.add_resource(InspectWorker, "/worker/<string:name>")
worker_api.add_resource(ManageWorker, "/worker")
