from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

#postgresql://postgres:enchantix@localhost/defstruct-local
url = os.environ['DATABASE_URL']
engine = create_engine(url)
session_factory = sessionmaker(bind=engine)

