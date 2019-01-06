from sqlalchemy import Integer, Column, String, create_engine, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json


dbconfig = json.load(open('config.json'))['database']

database_url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (
    dbconfig.get('username'),
    dbconfig.get('password'),
    dbconfig.get('host', '127.0.0.1'),
    dbconfig.get('port', 5432),
    dbconfig.get('name', 'leaderboard')
)

engine = create_engine(database_url)
Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    score = Column(Integer, default=0)
    streak = Column(Integer, default=0)


    def __str__(self):
        return '%s - %s - %s' % (self.username, self.score, self.streak)

    def __repr__(self):
        return '%s - %s - %s' % (self.username, self.score, self.streak)

    def add_score(self, session, points, date=None):
        import datetime

        if date is None:
            date = datetime.date.today()

        score = Score(username=self.username, score=points, date=date)
        session.add(score)
        self.score += points
        self.update_streak(session, date)
        self.streak = 1 if self.streak == 0 else self.streak + 1
        session.flush()
        session.commit()

    def update_streak(self, session, date=None):
        import datetime
        if date is None:
            date = datetime.date.today()
        last_score = session.query(Score).filter_by(username=self.username).\
            order_by(Score.date.desc()).first()
        if last_score.date < date - datetime.timedelta(days=1):
            self.streak = 0

    @staticmethod
    def get_leaders(session, offset=0, limit=50):
        from sqlalchemy import func
        rank_col = func.rank().over(order_by=User.score.desc()).label('rank')
        query = session.query(User).add_column(rank_col)
        results = query.offset(offset).limit(limit).all()
        return results

    def get_user_by_rank(session, rank):
        from sqlalchemy import func
        rank_col = func.rank().over(order_by=User.score.desc()).label('rank')
        query = session.query(User).add_column(rank_col)
        results = query.from_self().filter(rank_col==rank).all()
        return results

    @staticmethod
    def get_user_details(session, username, offset=5):
        from sqlalchemy import func
        rank_col = func.rank().over(order_by=User.score.desc()).label('rank')
        query = session.query(User).add_column(rank_col)
        user_row = query.from_self().filter(User.username==username).first()
        rank = user_row.rank
        # TODO: Limit number of results to 2*offset + 1 if there are multiple
        # users with same rank
        results = query.from_self().filter(rank_col>=rank-offset).\
            filter(rank_col<=rank+offset)
        return results.all()



class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey('users.username'))
    score = Column(Integer)
    date = Column(Date)

    def __str__(self):
        return '%s - %s - %s' % (self.username, self.score, self.date)

    def __repr__(self):
        return '%s - %s - %s' % (self.username, self.score, self.date)

