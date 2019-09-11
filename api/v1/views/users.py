#!/usr/bin/python3
''' starts a Flask web application '''
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, request, make_response, abort
from models import storage
from models.user import User


@app_views.route('/users/<user_id>',
                 methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
@app_views.route('/users', methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
def user_json(user_id=None):
    """
    Return in json format answers depending on a given request method
    Methods could be: GET, POST, PUT or DELETE
    """
    list_of_dict = []
    if request.method == 'GET' and user_id is None:
        for values in storage.all(User).values():
            list_of_dict.append(values.to_dict())
        return jsonify(list_of_dict)
    if request.method == 'GET' and user_id:
        single_dict = {}
        try:
            single_dict = storage.get('User', user_id).to_dict()
            return jsonify(single_dict)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)
    if request.method == 'DELETE' and user_id:
        try:
            single_dict = storage.get('User', user_id).delete()
            storage.save()
            return make_response(jsonify({}), 200)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)
    if request.method == 'POST' and user_id is None:
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            req = request.get_json()
            if 'name' not in req.keys():
                return make_response(jsonify({'error': 'Missing name'}), 400)
            if 'email' not in req.keys():
                return make_response(jsonify({'error': 'Missing email'}), 400)
            if 'password' not in req.keys():
                return make_response(jsonify({'error': 'Missing password'}),
                                     400)
            else:
                new_dict = User(**req)
                new_dict.save()
                return make_response(jsonify(new_dict.to_dict()), 201)

    if request.method == 'PUT' and user_id:
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            req = request.get_json()
            try:
                single_dict = storage.get('User', user_id)
                for key, val in req.items():
                    if key not in ["id", "created_at", "updated_at", "email"]:
                        setattr(single_dict, key, val)
                    else:
                        pass
                single_dict.save()
                return make_response(jsonify(single_dict.to_dict()), 200)
            except:
                return make_response(jsonify({'error': 'Not found'}), 404)
