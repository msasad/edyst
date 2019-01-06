from sqlalchemy import Integer, Column, String, create_engine, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#TODO Move out db connection parameters to a config file
engine = create_engine('postgresql+psycopg2://sid:password@127.0.0.1:5433/leaderboard')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    score = Column(Integer, default=0)
    streak = Column(Integer, default=0)

    def add_score(self, session, date, points):
        score = Score(username=self.username, score=points, date=date)
        session.add(score)
        self.score += points
        self.update_streak()
        self.streak = 1 if self.streak == 0 else self.streak + 1
        session.flush()
        session.commit()

    def update_streak(self, session):
        from datetime import date, timedelta
        last_score = session.query(Score).filter_by(username='foo').\
            order_by(Score.date.desc()).first()
        if last_score.date < date.today() - timedelta(days=1):
            self.streak = 0


class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey('users.username'))
    score = Column(Integer)
    date = Column(Date)
