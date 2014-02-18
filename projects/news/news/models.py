from sqlalchemy import Column, Unicode

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

maker = sessionmaker(extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

Base = declarative_base()

class DBConnect(object):
    def __init__(self, **settings):
        self.engine = engine_from_config(settings, 'sqlalchemy.')

    def connect(self):
        Base.metadata.bind = self.engine

    def create(self):
        Base.metadata.create_all(self.engine)        

class Visited(Base):
    __tablename__ = 'visited'

    url = Column(Unicode, primary_key=True)