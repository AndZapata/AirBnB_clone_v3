#!/usr/bin/python3
''' starts a Flask web application '''
from api.v1.views import app_views
from models.base_model import BaseModel
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
@app_views.route('/amenities', methods=['GET', 'POST', 'PUT', 'DELETE'],
                 strict_slashes=False)
def amenity_json(amenity_id=None):
    """
    Return in json format answers depending on a given request method
    Methods could be: GET, POST, PUT or DELETE
    """
    list_of_dict = []
    if request.method == 'GET' and amenity_id is None:
        for values in storage.all(Amenity).values():
            list_of_dict.append(values.to_dict())
        return jsonify(list_of_dict)
    if request.method == 'GET' and amenity_id:
        single_dict = {}
        try:
            single_dict = storage.get('Amenity', amenity_id).to_dict()
            return jsonify(single_dict)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)
    if request.method == 'DELETE' and amenity_id:
        try:
            single_dict = storage.get('Amenity', amenity_id).delete()
            storage.save()
            return make_response(jsonify({}), 200)
        except:
            return make_response(jsonify({'error': 'Not found'}), 404)
    if request.method == 'POST' and amenity_id is None:
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            req = request.get_json()
            if 'name' not in req.keys():
                return make_response(jsonify({'error': 'Missing name'}), 400)
            else:
                new_dict = Amenity(**req)
                new_dict.save()
                return make_response(jsonify(new_dict.to_dict()), 201)
    if request.method == 'PUT' and amenity_id:
        if not request.is_json:
            abort(400, 'Not a JSON')
        else:
            req = request.get_json()
            try:
                single_dict = storage.get('Amenity', amenity_id)
                for key, val in req.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(single_dict, key, val)
                    else:
                        pass
                single_dict.save()
                return make_response(jsonify(single_dict.to_dict()), 200)
            except:
                return make_response(jsonify({'error': 'Not found'}), 404)
