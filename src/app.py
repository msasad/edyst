import db
from flask import Flask, request, Response
from flask_restful import Resource, Api, abort
import json
import datetime
import click

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
                abort(400, reason='Failed to parse data. Invalid JSON')
        try:
            assert type(data['username']) == str
            assert int(data['points']) > 0
            date = datetime.datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S.%f')
            # Allowing future dates to test the 'streak' calculation
            # assert date <= datetime.datetime.now()
        except:
            abort(400, reason='Invalid values supplied.')
        try:
            session = db.Session()
            query = session.query(db.User).filter_by(username=data['username'])
            user = query.first()
            if user is None:
                user = db.User.create(session, username=data['username'])
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
                abort(404, reason='The specified user is not found')
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


# CLI Implementation


@app.cli.command()
def initdb():
    try:
        db.Base.metadata.create_all(db.engine)
    except:
        print('Failed to create tables, please check the database' +
        'configuration and try again')

@app.cli.command()
@click.argument('userfilename')
@click.argument('scoresfilename')
def loaddata(userfilename, scoresfilename):
    db.Base.metadata.create_all(db.engine)
    session = db.Session()
    with open(userfilename) as infile:
        for line in infile:
            username, score, streak = line.split(', ')
            score = int(score)
            streak = int(streak)
            user = db.User(username=username, score=score, streak=streak)
            session.add(user)
    session.flush()
    session.commit()

    with open(scoresfilename) as infile:
        for line in infile:
            username, score, date = line.split(', ')
            score = int(score)
            score_obj = db.Score(username=username, score=score, date=date)
            session.add(score_obj)
    session.flush()
    session.commit()
