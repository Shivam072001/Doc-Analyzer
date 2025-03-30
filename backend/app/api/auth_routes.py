from flask import Blueprint, request, jsonify, g, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import cross_origin
from bson.objectid import ObjectId
import jwt
import datetime
from ..core.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def generate_jwt(username):
    utc_now = datetime.datetime.now(datetime.timezone.utc) # Use timezone-aware UTC datetime
    payload = {
        'exp': utc_now + datetime.timedelta(hours=24),  # Token expiration time
        'iat': utc_now,
        'sub': username
    }
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256'
    )

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    users_collection = g.db.users

    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    users_collection.insert_one(new_user.to_dict())

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'message': 'Username and password are required',
            'status': 'failed'
            }), 400

    users_collection = g.db.users

    user_data = users_collection.find_one({'username': username})

    if user_data and check_password_hash(user_data['password'], password):
        token = generate_jwt(username)
        return jsonify({
            'message': 'Logged in successfully',
            'username': username,
            'token': token,
            'status': 'success'
        }), 200
    else:
        return jsonify({
            'message': 'Invalid username or password',
            'status': 'failed'
            }), 401