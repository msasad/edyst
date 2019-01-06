import db
from flask import Flask, request
from flask_restful import Resource, Api, abort
import json
import datetime

app = Flask(__name__)
api = Api(app)


class Results(Resource):
    def post(self):
        # TODO: Handle each type of exception in separate handler blocks
        if request.json:
            data = request.json
        else:
            try:
                data = json.loads(request.data)
            except:
                abort(400)
        try:
            assert type(data['username']) == str
            assert int(data['points']) > 0
            assert datetime.date.fromisoformat(data['date']) <= datetime.date.today()
        except:
            abort(400)
        return dict(this='that')

api.add_resource(Results, '/api/results')

