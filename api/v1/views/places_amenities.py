#!/usr/bin/python3
''' starts a Flask web application '''
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def places_amenity_get(place_id):
    """
    Return in json format response
    """
    list_of_dict = []
    single_dict = storage.get('Place', place_id)
    if not single_dict:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity = single_dict.amenities
    else:
        amenity = single_dict.amenity_ids
    for val in amenity:
        list_of_dict.append(val.to_dict())
    return jsonify(list_of_dict)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def places_amenity_delete(place_id, amenity_id):
    """
    Return in json format response
    """
    single_dict_pl = storage.get('Place', place_id)
    if single_dict_pl is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    single_dict_am = storage.get('Amenity', amenity_id)
    if not single_dict_am:
        return make_response(jsonify({'error': 'Not found'}), 404)
    for single_dict_pl in single_dict_pl.amenities:
        if single_dict_pl.id == amenity_id:
            single_dict_pl.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'],
                 strict_slashes=False)
def places_amenity_post(place_id, amenity_id):
    """
    Return in json format response
    """
    single_dict_pl = storage.get('Place', place_id)
    if single_dict_pl is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    single_dict_am = storage.get('Amenity', amenity_id)
    if not single_dict_am:
        return make_response(jsonify({'error': 'Not found'}), 404)
    for single_dict_pl in single_dict_pl.amenities:
        if single_dict_pl.id == amenity_id:
            return make_response(jsonify(single_dict_pl.to_dict()), 200)
