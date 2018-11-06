import random
import string
import json

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash

from app.utils.helper import login_session
from . import session, asc
from app import app
from app.models.user import User
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant

# Show all restaurants
#JSON APIs

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/restaurant/JSON')
def restaurants_json():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


@app.route('/')
@app.route('/restaurant/')
def show_restaurants():
    restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    if 'username' not in login_session:
        return render_template(
            'publicrestaurants.html',
            restaurants=restaurants)
    else:
        return render_template('restaurants.html', restaurants=restaurants)

# Create a new restaurant


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def create_new_restaurant():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        create_new_restaurant = Restaurant(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(create_new_restaurant)
        flash(
            'New Restaurant %s Successfully Created' %
            create_new_restaurant.name)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('newRestaurant.html')

# Edit a restaurant


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    edited_restaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if edited_restaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            edited_restaurant.name = request.form['name']
            flash('Restaurant Successfully Edited %s' % edited_restaurant.name)
            return redirect(url_for('show_restaurants'))
    else:
        return render_template(
            'editRestaurant.html',
            restaurant=edited_restaurant)


# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant_to_be_delete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if restaurant_to_be_delete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(restaurant_to_be_delete)
        flash('%s Successfully Deleted' % restaurant_to_be_delete.name)
        session.commit()
        return redirect(
            url_for(
                'show_restaurants',
                restaurant_id=restaurant_id))
    else:
        return render_template(
            'deleteRestaurant.html',
            restaurant=restaurant_to_be_delete)
