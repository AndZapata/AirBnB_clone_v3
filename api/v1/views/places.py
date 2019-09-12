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


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """
    Return in json format answers depending on a given request method
    Methods could be: GET, POST
    """
    if request.method == 'GET' and city_id:
        list_of_dict = []
        try:
            single_dict = storage.get('City', city_id)
            for val in single_dict.places:
                list_of_dict.append(val.to_dict())
            return jsonify(list_of_dict)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)
    if request.method == 'POST' and city_id:
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            single_dict = storage.get('City', city_id)
            if not single_dict:
                return make_response(jsonify({'error': 'Not found'}), 404)
            req = request.get_json()
            if 'user_id' not in req.keys():
                return make_response(jsonify({'error': 'Missing user_id'}),
                                     400)
            value_id = req.get('user_id')
            if not storage.get('User', value_id):
                return make_response(jsonify({'error': 'Not found'}), 404)
            if 'name' not in req.keys():
                return make_response(jsonify({'error': 'Missing name'}), 400)
            else:
                req['city_id'] = city_id
                new_dict = Place(**req)
                new_dict.save()
                return make_response(jsonify(new_dict.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def places_json(place_id):
    """ comment cool """
    if request.method == 'GET' and place_id:
        single_dict = storage.get('Place', place_id)
        if not single_dict:
            return make_response(jsonify({'error': 'Not found'}), 404)
        return jsonify(single_dict.to_dict())
    if request.method == 'DELETE' and place_id:
        try:
            single_dict = storage.get('Place', place_id).delete()
            storage.save()
            return make_response(jsonify({}), 200)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)

    if request.method == 'PUT' and place_id:
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            req = request.get_json()
            try:
                single_dict = storage.get('Place', place_id)
                for key, val in req.items():
                    if key not in ["id", "user_id", "city_id",
                                   "created_at", "updated_at"]:
                        setattr(single_dict, key, val)
                    else:
                        pass
                single_dict.save()
                return make_response(jsonify(single_dict.to_dict()), 200)
            except:
                return make_response(jsonify({'error': 'Not found'}), 404)
