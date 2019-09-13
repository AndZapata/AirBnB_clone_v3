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
    if not single_dict_pl:
        return make_response(jsonify({'error': 'Not found'}), 404)
    #if amenity_id not in [single_dict_pl.amenities, single_dict_pl.amenity_ids:
        #return make_response(jsonify({'error': 'Not found'}), 404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        all_amenity = single_dict_pl.amenities
    else:
        all_amenity = single_dict_pl.amenity_ids
    single_dict_am = all_amenity.get('Amenity', amenity_id)
    if not single_dict_am:
        return make_response(jsonify({'error': 'Not found'}), 404)
    single_dict_am.delete()
    #storage.save()
    return make_response(jsonify({}), 200)

    """
    if request.method == 'POST' and place_id:
    if not request.is_json:
    abort(400, 'Not a JSON')
    else:
            single_dict = storage.get('Place', place_id)
            if not single_dict:
                return make_response(jsonify({'error': 'Not found'}), 404)
            req = request.get_json()
            if 'user_id' not in req.keys():
                return make_response(jsonify({'error': 'Missing user_id'}),
                                     400)
            value_id = req.get('user_id')
            if not storage.get('User', value_id):
                return make_response(jsonify({'error': 'Not found'}), 404)
            if 'text' not in req.keys():
                return make_response(jsonify({'error': 'Missing text'}), 400)
            else:
                req.update({'place_id': place_id})
                new_dict = Review(**req)
                new_dict.save()
                return make_response(jsonify(new_dict.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def reviews_json(review_id):

    if request.method == 'GET' and review_id:
        single_dict = storage.get('Review', review_id)
        if not single_dict:
            return make_response(jsonify({'error': 'Not found'}), 404)
        return jsonify(single_dict.to_dict())
    if request.method == 'DELETE' and review_id:
        try:
            single_dict = storage.get('Review', review_id).delete()
            storage.save()
            return make_response(jsonify({}), 200)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)

    if request.method == 'PUT' and review_id:
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            req = request.get_json()
            try:
                single_dict = storage.get('Review', review_id)
                for key, val in req.items():
                    if key not in ["id", "user_id", "place_id",
                                   "created_at", "updated_at"]:
                        setattr(single_dict, key, val)
                    else:
                        pass
                single_dict.save()
                return make_response(jsonify(single_dict.to_dict()), 200)
            except:
                return make_response(jsonify({'error': 'Not found'}), 404)"""
