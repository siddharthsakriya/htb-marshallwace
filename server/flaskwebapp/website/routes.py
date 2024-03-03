from flask import Blueprint, request, jsonify
from .db_util.user import create_user, read_user
import json

routes = Blueprint('routes', __name__)

#User routes
@routes.route('/register_user', methods=['POST'])
def register_user():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        user = create_user(email, password)
        return jsonify(serialize_user(user))
    
@routes.route('/login_user', methods=['POST'])
def login_user_now():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        user = read_user(email)
        if user and user.password == password:
            return jsonify(serialize_user(user))
        else:
            return jsonify({'user': None})    

@routes.route('/read_user', methods=['POST'])
def read_user_now():
    if request.method == 'POST':
        email = request.json['email']
        user = read_user(email)
        return jsonify(serialize_user(user))

#as user is not serialisable on it's own, we need to create a function to serialise it
def serialize_user(user):
        return {"id": user.id,
                "email": user.email,
                }
