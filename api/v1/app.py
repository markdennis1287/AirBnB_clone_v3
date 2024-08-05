#!/usr/bin/python3
"""

"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_engine(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error """
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(debug=True,host=HOST, port=PORT, threaded=True)