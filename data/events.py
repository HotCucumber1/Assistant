import datetime as dt
import sqlalchemy
from sqlalchemy import Integer, String, Date, Time
from .db_session import SqlAlchemyBase


class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    event_name = sqlalchemy.Column(String, nullable=False, unique=True)
    number_of_notes = sqlalchemy.Column(Integer, nullable=True)
    date = sqlalchemy.Column(Date, nullable=True)
    time = sqlalchemy.Column(Time, nullable=True)