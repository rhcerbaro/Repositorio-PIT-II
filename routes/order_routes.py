from flask import Blueprint, jsonify, request
from models.order import create_order
from utils.notifications import send_notification

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods=['POST'])
def make_order():
    data = request.get_json()
    order = create_order(data['user_id'], data['items'])
    send_notification(data['user_id'], 'Pedido Realizado com sucesso')
    return jsonify({'message': 'Pedido criado', 'order': order}), 201
