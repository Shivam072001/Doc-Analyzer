from flask import current_app, request, jsonify
import jwt
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("Inside token_required decorator")  # Debugging line 1
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
                print ("token: ", token) # Debugging line 2
            except IndexError:
                return jsonify({'message': 'Bearer token not found!'}), 401

        if not token:
            print("Token is missing") # Debugging line 3
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data.get('user_id') # Assuming 'user_id' is in your JWT payload
            if not current_user_id:
                print("Invalid token payload") # Debugging line 4
                return jsonify({'message': 'Invalid token payload'}), 401
        except jwt.ExpiredSignatureError:
            print("Token has expired") # Debugging line 5
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            print("Invalid token") # Debugging line 6
            return jsonify({'message': 'Invalid token!'}), 401

        print("Token is valid, proceeding to route") # Debugging line 7
        return f(current_user_id, *args, **kwargs) # Pass the user_id to the route function

    return decorated