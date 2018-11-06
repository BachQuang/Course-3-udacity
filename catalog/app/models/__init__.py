from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from menu_item import MenuItem
from restaurant import Restaurant
from user import User