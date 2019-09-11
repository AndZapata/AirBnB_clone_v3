#!/usr/bin/python3
''' starts a Flask web application '''
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')


@app.errorhandler(404)
def not_found(error):
    """
    Gives error message when any invalid url are requested
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def session_close(error):
    ''' close the session '''
    storage.close()

if __name__ == '__main__':
    app.run(host=host, port=(int(port)), threaded=True)
