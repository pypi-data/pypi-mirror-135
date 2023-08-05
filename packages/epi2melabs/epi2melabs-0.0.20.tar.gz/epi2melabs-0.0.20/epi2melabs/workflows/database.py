# flake8: noqa
import datetime
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


@dataclass
class Statuses:
    UNKNOWN = 'UNKNOWN'
    LAUNCHED = 'LAUNCHED'
    ENCOUNTERED_ERROR = 'ENCOUNTERED_ERROR'
    COMPLETED_SUCCESSFULLY = 'COMPLETED_SUCCESSFULLY'
    TERMINATED = 'TERMINATED'


class Instance(Base):
    __tablename__ = 'instances'

    id = Column(String, primary_key=True)
    pid = Column(Integer, nullable=True)
    path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    workflow = Column(String, nullable=False)
    status = Column(String, default=Statuses.UNKNOWN)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.utcnow)

    def __init__(self, id, path, name, workflow):
        self.id = id
        self.path = path
        self.name = name
        self.workflow = workflow

    def to_dict(self):
        return {
            'id': self.id,
            'path': self.path,
            'name': self.name,
            'status': self.status,
            'workflow': self.workflow,
            'created_at': self.created_at.strftime("%Y-%m-%d-%H-%M"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d-%H-%M")
        }

    def __repr__(self):
        return '<Instance %r>' % self.id


def get_session(uri):
    engine = create_engine(uri)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

