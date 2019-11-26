from sqlalchemy import Column, String, Integer, DateTime, Time, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from utils.base import Base

#-----------------------------------------------------------------------------

class User(Base):
    __tablename__ = 'users'

    net_id = Column(String(200), primary_key=True, unique=True)

    # one to many relationship with template instances
    temp_instances = relationship("TempInstance", backref='owner')

    # one to many relationship with requests
    requests = relationship("Request", backref='owner')
    
    def __repr__(self):
        return '<User %r>' % self.net_id

#-----------------------------------------------------------------------------

class TempInstance(Base):
    __tablename__ = 'temp_instances'

    instance_id = Column(Integer, primary_key=True, unique=True)
    owner_id = Column(String(200), ForeignKey('users.net_id'))
    partner_id = Column(String(200), nullable=True)
    template_id = Column(Integer, ForeignKey('templates.temp_id'))
    request_id = Column(Integer, ForeignKey('requests.request_id'))
    dueDate = Column(DateTime, nullable=False)
    savedState = Column(Text, nullable=False)

    def __repr__(self):
        return '<TempInstance %r> owned by %r, displaying template %r' % (self.instance_id, self.owner_id, self.template_id) 
#-----------------------------------------------------------------------------

class Template(Base):
    __tablename__ = 'templates'

    temp_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(500), nullable=False)
    html = Column(Text, nullable=False)

    # one to many relationship with instances
    tempinstance = relationship("TempInstance", backref='template')
    def __repr__(self):
        return '<Template %r> %r' % (self.temp_id, self.name)

#-----------------------------------------------------------------------------
class Request(Base):
    __tablename__ = 'requests'

    request_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    # many to one relationship w/ user
    sender_id = Column(String(200), ForeignKey('users.net_id'))
    receiver_id = Column(String(200), nullable=False)

    # one to one relationship w/ a request
    instance = relationship("TempInstance", uselist=False, backref='request')

    def __repr__(self):
        return '<Request %r from %r to %r>' % (self.request_id, self.sender_id, self.receiver_id)
    # temp_id = Column(Integer, ForeignKey('temp_instances.instance_id'))
    # one to one relationship w/ a template instance
    # template = relationship("TempInstance", backref=backref("temp_instance", uselist=False))

