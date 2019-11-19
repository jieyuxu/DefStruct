from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#postgresql://postgres:enchantix@localhost/defstruct-local
engine = create_engine('postgresql://postgres:enchantix@localhost:5555/defstruct-local')
Session = sessionmaker(bind=engine)

Base = declarative_base()