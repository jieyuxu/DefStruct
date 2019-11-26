from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

#postgresql://postgres:enchantix@localhost/defstruct-local
engine = create_engine('postgresql://postgres:enchantix@localhost:5555/defstruct-local')
session_factory = sessionmaker(bind=engine)

