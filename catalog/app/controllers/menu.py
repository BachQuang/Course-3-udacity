import random
import string
import httplib2
import json
import requests

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask import make_response

from . import session, asc
from app.utils.helper import login_session, get_user_info, authenticated, authorized
from app import app
from app.models.user import User
from app.models.menu_item import MenuItem
from app.models.restaurant import Restaurant


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
@authenticated
def show_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    creator = get_user_info(restaurant.user_id)
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    if  creator.id != login_session['user_id']:
        return render_template(
            'publicmenu.html',
            items=items,
            restaurant=restaurant,
            creator=creator)
    else:
        return render_template(
            'menu.html',
            items=items,
            restaurant=restaurant,
            creator=creator)


# Create a new menu item
@app.route(
    '/restaurant/<int:restaurant_id>/menu/new/',
    methods=[
        'GET',
        'POST'])
@authorized
@authenticated
def create_new_menu(restaurant_id):
    if request.method == 'POST':
        if request.form['name']:
            name = request.form['name']
        if request.form['description']:
            description = request.form['description']
        if request.form['price']:
            price = request.form['price']
        if request.form['course']:
            course = request.form['course']
        
        newItem = MenuItem(
            name = name,
            description = description,
            price = price,
            course = course,
            restaurant_id = restaurant_id,
            user_id = restaurant.user_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Edit a menu item


@app.route(
    '/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
    methods=[
        'GET',
        'POST'])
@authorized
@authenticated
def edit_menu_item(restaurant_id, menu_id):
    edited_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        if request.form['description']:
            edited_item.description = request.form['description']
        if request.form['price']:
            edited_item.price = request.form['price']
        if request.form['course']:
            edited_item.course = request.form['course']
        session.add(edited_item)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html',
            restaurant_id=restaurant_id,
            menu_id=menu_id,
            item=edited_item)


# Delete a menu item
@app.route(
    '/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',
    methods=[
        'GET',
        'POST'])
@authorized
@authenticated
def delete_menu_item(restaurant_id, menu_id):
    item_to_be_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item_to_be_delete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=item_to_be_delete)
