import json

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from app.models import Base


# Connect to Database
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from authentication import *
from restaurant import *
from menu import *
