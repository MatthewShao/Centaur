from flask import Blueprint, jsonify, make_response
from flask.ext.restful import Api, Resource
from Server.db import client
import json

result_bp = Blueprint('result', __name__)
result_api = Api(result_bp)
result_db = client.centaur


class UpdateResult(Resource):

    def post(self):
        celery_stored = result_db.celery_taskmeta.find()
        for item in celery_stored:
            result = json.loads(item["result"])
            result_dict = {
                "url": result[0],
                "poc": result[1],
                "code": result[2][0],
                "msg": result[2][1],
                "endtime": result[3],
                "return": result[4]
            }
            try:
                result_db.results.insert_one(result_dict)
                result_db.celery_taskmeta.delete_one({"_id":item["_id"]})
            except Exception,e:
                return make_response(jsonify({"msg":e}))
        return make_response(jsonify({"msg":"success"}))


result_api.add_resource(UpdateResult, '/result')


