import sqlalchemy
from sqlalchemy import orm
from sqlalchemy import Integer, String
from .db_session import SqlAlchemyBase


class Note(SqlAlchemyBase):
    __tablename__ = "notes"

    id = sqlalchemy.Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    note_name = sqlalchemy.Column(Integer, nullable=False)
    event_id = sqlalchemy.Column(Integer, sqlalchemy.ForeignKey("events.id"), nullable=True)

    event = orm.relationship("Event")
