from flask import session as login_session, redirect

from app.models.user import User
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant
from app.controllers import session
from functools import wraps

# User Helper Functions


def create_user(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None

def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        else:
            return func(*args, **kwargs)
    
    return wrapper

def authorized(func):
    @wraps(func)
    def wrapper(restaurant_id, *args, **kwargs):
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        if login_session['user_id'] != restaurant.user_id:
            return redirect('/restaurant')
        else:
            return func(restaurant_id, *args, **kwargs)
    return wrapper