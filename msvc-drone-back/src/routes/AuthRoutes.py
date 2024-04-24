from flask import Blueprint, request, jsonify

from src.services.AuthenticationService import AuthenticationService

main = Blueprint('auth_blueprint', __name__)


@main.route('/token', methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json['password']

    encoded_token = AuthenticationService.login_user(username, password)

    if encoded_token is not None:
        return jsonify({'success': True, 'token': encoded_token})
    else:
        response = jsonify({'message': 'Invalid credentials'})
        return response, 401


@main.route('/sign-up', methods=['POST'])
def sign_up():
    fullname = request.json["fullname"]
    username = request.json["username"]
    password = request.json["password"]
    role = request.json["role"]
    email = request.json["email"]

    res = AuthenticationService.sign_up(fullname, username, password, role, email)
    if res:
        return '', 201
    else:
        response = jsonify({'message': 'Unexpected error'})
        return response, 400
