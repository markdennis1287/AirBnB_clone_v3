#!/usr/bin/python3
"""

"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_all_users():
    """ get all users """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """ get user by id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """ delete user by id """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """ create user """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        return abort(400, 'Not a JSON')
    if 'email' not in data:
        return abort(400, 'Missing email')
    if 'password' not in data:
        return abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """ update user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        return abort(400, 'Not a JSON')
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

