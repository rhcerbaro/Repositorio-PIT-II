database = {'orders': []}

def create_order(user_id, items):
    order = {
        'id': len(database['orders']) + 1,
        'user_id': user_id,
        'items': items,
        'total': sum(item['price'] for item in items),
        'status': 'Pedido Realizado'
    }
    database['orders'].append(order)
    return order
