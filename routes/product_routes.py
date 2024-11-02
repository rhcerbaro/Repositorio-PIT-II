from flask import Blueprint, jsonify, request
from models.product import rate_product

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/<int:product_id>/rate', methods=['POST'])
def rate(product_id):
    data = request.get_json()
    product = rate_product(product_id, data['user_id'], data['rating'])
    if product:
        return jsonify({'message': 'Avaliação registrada'}), 200
    return jsonify({'error': 'Produto não encontrado'}), 404
