#!/usr/bin/python3
''' starts a Flask web application '''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.user import User


@app_views.route('/status')
def status_json():
    """ Checking the status in json format """
    return jsonify(status='OK')


@app_views.route('/stats')
def counter():
    """ Count the number of object for each class """
    new_dict = {}
    cls = {'amenities': Amenity, 'cities': City, 'places': Place,
           'reviews': Review, 'states': State, 'users': User}
    for key, val in cls.items():
        new_dict[key] = storage.count(val)
    return jsonify(new_dict)
