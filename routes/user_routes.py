from flask import Blueprint, jsonify, request
from models.user import create_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user = create_user(data)
    return jsonify({'message': 'Usuário registrado com sucesso', 'user': user}), 201
