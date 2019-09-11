#!/usr/bin/python3
''' starts a Flask web application '''
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, request, make_response
from models import storage
from models.state import State


@app_views.route('/states/<state_id>',
                 methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
@app_views.route('/states', methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
def states_json(state_id=None):
    """
    Return in json format answers depending on a given request method
    Methods could be: GET, POST, PUT or DELETE
    """
    list_of_dict = []
    if request.method == 'GET' and state_id is None:
        for values in storage.all(State).values():
            list_of_dict.append(values.to_dict())
        return jsonify(list_of_dict)
    if request.method == 'GET' and state_id:
        single_dict = {}
        try:
            single_dict = storage.get('State', state_id).to_dict()
            return jsonify(single_dict)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)
    if request.method == 'DELETE' and state_id:
        try:
            single_dict = storage.get('State', state_id).delete()
            storage.save()
            return make_response(jsonify({}), 200)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)
    if request.method == 'POST' and state_id is None:
        try:
            req = request.get_json()
            if 'name' not in req.keys():
                return make_response(jsonify({'error': 'Missing name'}), 400)
            else:
                new_dict = State(**req)
                new_dict.save()
                return make_response(jsonify(new_dict.to_dict()), 201)
        except:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if request.method == 'PUT' and state_id:
        try:
            req = request.get_json()
            try:
                single_dict = storage.get('State', state_id)
                for key, val in req.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(single_dict, key, val)
                    else:
                        pass
                single_dict.save()
                return make_response(jsonify(single_dict.to_dict()), 200)
            except:
                return make_response(jsonify({'error': 'Not found'}), 404)
        except:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
