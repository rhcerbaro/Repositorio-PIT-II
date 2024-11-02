from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_session import Session
from database import db, init_db, User, Product, Order, Rating
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafeteria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
init_db(app)

# Função para inicializar produtos no banco de dados
def create_initial_products():
    if not Product.query.first():
        products = [
            Product(name="Espresso", price=3.0, description="Café concentrado e forte."),
            Product(name="Cappuccino", price=4.5, description="Café com leite vaporizado e espuma."),
            Product(name="Latte", price=4.0, description="Café suave com leite vaporizado."),
            Product(name="Mocha", price=4.5, description="Café com chocolate e chantilly."),
            Product(name="Macchiato", price=3.5, description="Espresso com toque de leite."),
            Product(name="Americano", price=3.0, description="Espresso diluído em água quente."),
            Product(name="Flat White", price=4.0, description="Café com leite vaporizado."),
            Product(name="Affogato", price=5.0, description="Espresso sobre sorvete."),
            Product(name="Irish Coffee", price=6.0, description="Café com whisky e chantilly."),
            Product(name="Iced Coffee", price=3.5, description="Café gelado.")
        ]
        db.session.bulk_save_objects(products)
        db.session.commit()

# Chama a função para garantir que o banco tenha produtos ao iniciar o app
with app.app_context():
    create_initial_products()

# Página inicial com links para funcionalidades
@app.route('/')
def home():
    return '''
    <!doctype html>
    <html lang="pt-BR">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Bem-vindo ao Gourmetz API</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; }
            h1 { text-align: center; color: #444; margin-top: 30px; }
            .container { max-width: 800px; margin: 0 auto; padding: 20px; }
            .links { list-style-type: none; padding: 0; }
            .links li { margin: 15px 0; }
            .links a { text-decoration: none; color: #0056b3; font-size: 18px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bem-vindo ao Gourmetz API</h1>
            <ul class="links">
                <li><strong>Registro de Usuário:</strong> <a href="/user/register">/user/register</a></li>
                <li><strong>Login de Usuário:</strong> <a href="/user/login">/user/login</a></li>
                <li><strong>Cardápio de Cafés:</strong> <a href="/menu">/menu</a></li>
                <li><strong>Criar Pedido:</strong> <a href="/order/create">/order/create</a></li>
                <li><strong>Histórico de Pedidos:</strong> <a href="/order/history">/order/history</a></li>
                <li><strong>Avaliar Produtos:</strong> <a href="/product/1/rate">/product/&lt;product_id&gt;/rate</a></li>
            </ul>
        </div>
    </body>
    </html>
    '''

# Função de registro de usuário
@app.route('/user/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template_string('<h1>Erro: Este e-mail já está em uso. Tente outro.</h1>')

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return render_template_string(f'<h1>Usuário registrado com sucesso! Seu ID de usuário é: {new_user.id}</h1>')
    
    return '''
    <form method="POST">
        <label for="name">Nome:</label><input type="text" name="name" required><br>
        <label for="email">Email:</label><input type="email" name="email" required><br>
        <label for="password">Senha:</label><input type="password" name="password" required><br>
        <button type="submit">Registrar</button>
    </form>
    '''

# Função de login de usuário
@app.route('/user/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return render_template_string(f'<h1>Login bem-sucedido! Seu ID de usuário é: {user.id}</h1>')
        return render_template_string('<h1>Falha no login. Tente novamente.</h1>')
    
    return '''
    <form method="POST">
        <label for="email">Email:</label><input type="email" name="email" required><br>
        <label for="password">Senha:</label><input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    '''

# Exibição do cardápio de cafés
@app.route('/menu')
def menu():
    menu_template = '''
    <!doctype html>
    <html lang="pt-BR">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Cardápio de Cafés</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f3f4f6; }
            h1 { text-align: center; color: #333; }
            .menu-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 20px; }
            .coffee-card { background-color: #fff; border: 1px solid #ddd; padding: 15px; width: 200px; text-align: center; }
            .coffee-card h3 { color: #555; margin: 10px 0; }
            .coffee-card p { color: #777; font-size: 14px; }
            .coffee-card .id { font-size: 12px; color: #999; }
        </style>
    </head>
    <body>
        <h1>Cardápio de Cafés</h1>
        <div class="menu-container">
            {% for coffee in coffees %}
                <div class="coffee-card">
                    <div class="id">ID: {{ coffee.id }}</div>
                    <h3>{{ coffee.name }} - R$ {{ coffee.price }}</h3>
                    <p>{{ coffee.description }}</p>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    coffees = Product.query.all()
    return render_template_string(menu_template, coffees=coffees)

# Criação de pedidos com base no ID do café
@app.route('/order/create', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login_user'))
        
        product_ids = request.form.getlist('product_ids')
        total = 0
        products = []

        for product_id in product_ids:
            product = Product.query.get(int(product_id))
            if product:
                products.append(product)
                total += product.price
        
        new_order = Order(user_id=user_id, total=total, products=products)
        db.session.add(new_order)
        db.session.commit()
        
        return render_template_string(f'<h1>Pedido criado com sucesso! Total: R$ {total}</h1>')
    
    products = Product.query.all()
    product_options = ''.join([f'<option value="{p.id}">{p.id} - {p.name} - R$ {p.price}</option>' for p in products])
    
    return f'''
    <form method="POST">
        <label for="product_ids">Escolha os Produtos:</label><select name="product_ids" multiple>{product_options}</select><br>
        <button type="submit">Criar Pedido</button>
    </form>
    '''

# Histórico de pedidos para o usuário logado
@app.route('/order/history')
def order_history():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login_user'))

    orders = Order.query.filter_by(user_id=user_id).all()
    history_template = '''
    <!doctype html>
    <html lang="pt-BR">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Histórico de Pedidos</title>
        <style>
            body { font-family: Arial, sans-serif; }
            h1 { text-align: center; }
            .order { border: 1px solid #ddd; padding: 10px; margin: 10px; }
            .order-products { font-size: 14px; color: #555; }
        </style>
    </head>
    <body>
        <h1>Histórico de Pedidos</h1>
        {% for order in orders %}
            <div class="order">
                <p><strong>ID do Pedido:</strong> {{ order.id }}</p>
                <p><strong>Total:</strong> R$ {{ order.total }}</p>
                <p class="order-products"><strong>Produtos:</strong>
                    <ul>
                        {% for product in order.products %}
                            <li>{{ product.name }} - R$ {{ product.price }}</li>
                        {% endfor %}
                    </ul>
                </p>
            </div>
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(history_template, orders=orders)

# Avaliação de produtos
@app.route('/product/<int:product_id>/rate', methods=['GET', 'POST'])
def rate_product(product_id):
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return redirect(url_for('login_user'))
        
        rating_value = int(request.form.get('rating'))
        comment = request.form.get('comment')
        
        has_purchased = Order.query.filter(Order.user_id == user_id, Order.products.any(id=product_id)).first()
        
        if has_purchased:
            rating = Rating(product_id=product_id, user_id=user_id, rating=rating_value, comment=comment)
            db.session.add(rating)
            db.session.commit()
            return render_template_string('<h1>Avaliação enviada com sucesso!</h1>')
        else:
            return render_template_string('<h1>Você só pode avaliar produtos comprados.</h1>')
    
    return '''
    <form method="POST">
        <label for="rating">Nota:</label><input type="number" name="rating" min="1" max="5" required><br>
        <label for="comment">Comentário:</label><textarea name="comment"></textarea><br>
        <button type="submit">Enviar Avaliação</button>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
