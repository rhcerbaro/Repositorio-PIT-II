database = {'products': [{'id': 1, 'name': 'Café Espresso', 'price': 5.0}]}

def rate_product(product_id, user_id, rating):
    product = next((p for p in database['products'] if p['id'] == product_id), None)
    if product:
        product.setdefault('ratings', []).append({'user_id': user_id, 'rating': rating})
        return product
    return None
