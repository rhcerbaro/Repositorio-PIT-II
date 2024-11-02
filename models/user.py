database = {'users': []}

def create_user(data):
    user = {
        'id': len(database['users']) + 1,
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    database['users'].append(user)
    return user
