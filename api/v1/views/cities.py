#!/usr/bin/python3
''' starts a Flask web application '''
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def states_cities(state_id):
    """
    Return in json format answers depending on a given request method
    Methods could be: GET, POST, PUT or DELETE
    """
    if request.method == 'GET' and state_id:
        list_of_dict = []
        try:
            single_dict = storage.get('State', state_id)
            for val in single_dict.cities:
                list_of_dict.append(val.to_dict())
            return jsonify(list_of_dict)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)
    if request.method == 'POST':
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            single_dict = storage.get('State', state_id)
            if not single_dict:
                return make_response(jsonify({'error': 'Not found'}), 404)
            req = request.get_json()
            if 'name' not in req.keys():
                return make_response(jsonify({'error': 'Missing name'}), 400)
            else:
                req['state_id'] = state_id
                new_dict = City(**req)
                new_dict.save()
                return make_response(jsonify(new_dict.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def cities_json(city_id):
    """ comment cool """
    if request.method == 'GET':
        single_dict = storage.get('City', city_id)
        if not single_dict:
            return make_response(jsonify({'error': 'Not found'}), 404)
        return jsonify(single_dict.to_dict())
    if request.method == 'DELETE' and city_id:
        try:
            single_dict = storage.get('City', city_id).delete()
            storage.save()
            return make_response(jsonify({}), 200)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)

    if request.method == 'PUT' and city_id:
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            req = request.get_json()
            try:
                single_dict = storage.get('City', city_id)
                for key, val in req.items():
                    if key not in ["id", "state_id",
                                   "created_at", "updated_at"]:
                        setattr(single_dict, key, val)
                    else:
                        pass
                single_dict.save()
                return make_response(jsonify(single_dict.to_dict()), 200)
            except:
                return make_response(jsonify({'error': 'Not found'}), 404)
