import db
from flask import Flask, request, Response
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
            date = datetime.date.fromisoformat(data['date'])
            # Allowing future dates to test the 'streak' calculation
            # assert date <= datetime.date.today()
        except:
            abort(400)
        try:
            session = db.Session()
            query = session.query(db.User).filter_by(username=data['username'])
            user = query.first()
            if user is None:
                abort(400)
            else:
                user.add_score(session, data['points'], date)
        except:
            abort(500)
        response = Response(status=201)
        return response

api.add_resource(Results, '/api/results')


class LeaderboardAll(Resource):
    def get(self, page=1, perpage=50):
        session = db.Session()
        offset = (page - 1) * perpage
        rows = db.User.get_leaders(session, offset, perpage)
        payload = []
        for row in rows:
            row.User.update_streak(session)
            entry = {}
            entry['username'] = row.User.username
            entry['total_points'] = row.User.score
            entry['streak'] = row.User.streak
            entry['rank'] = row.rank
            payload.append(entry)
        return Response(json.dumps(payload), mimetype='application/json')

api.add_resource(LeaderboardAll, '/api/leaderboard/all/',
                 '/api/leaderboard/all/<int:page>')


class LeaderboardUser(Resource):
    def get(self, param):
        session = db.Session()
        try:
            param = int(param)
            rows = db.User.get_user_by_rank(session, param)
        except ValueError:
            try:
                rows = db.User.get_user_details(session, param)
            except db.User.NotFound:
                abort(404)
        payload = []
        for row in rows:
            entry = {}
            row.User.update_streak(session)
            entry['username'] = row.User.username
            entry['total_points'] = row.User.score
            entry['streak'] = row.User.streak
            entry['rank'] = row.rank
            payload.append(entry)
        return Response(json.dumps(payload), mimetype='application/json')

api.add_resource(LeaderboardUser, '/api/leaderboard/<param>')
