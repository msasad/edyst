from sqlalchemy import Integer, Column, String, create_engine, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql+psycopg2://sid:password@127.0.0.1:5433/leaderboard')
Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    score = Column(Integer, default=0)
    streak = Column(Integer, default=0)

    def add_score(self, date, points, session):
        score = Score(username=self.username, score=points, date=date)
        session.add(score)
        self.score += points
        self.streak = 1 if self.streak == 0 else self.streak + 1
        # session.add(self)
        session.flush()
        session.commit()


class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey('users.username'))
    score = Column(Integer)
    date = Column(Date)
