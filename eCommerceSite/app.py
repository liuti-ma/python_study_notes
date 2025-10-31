# app.py
from os import abort

from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
import stripe
from flask_wtf import FlaskForm
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize extensions

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Stripe configuration
stripe.api_key = app.config['STRIPE_SECRET_KEY']
# User model
class Base(DeclarativeBase):
    pass
login_manager = LoginManager(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)
@login_manager.user_loader  # <-- THIS IS CRUCIAL
def load_user(user_id):
    return User.query.get(int(user_id))
# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)  # in cents
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stripe_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    items = db.relationship('OrderItem', backref='order', lazy=True)

# Order item model
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')

with app.app_context():
    db.create_all()
    print(load_user(1))  # Should return User object or None
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Handle registration form
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=request.form['username'],
                    email=request.form['email'],
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('account'))
        else:
            flash('Login failed. Check email and password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    # Add product to cart session
    cart = session['cart']
    cart.append(product_id)
    session['cart'] = cart
    flash('Item added to cart!', 'success')
    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    if 'cart' not in session:
        return render_template('cart.html', products=[], total=0)

    # Get products from cart session
    cart_items = {}
    for product_id in session['cart']:
        if product_id in cart_items:
            cart_items[product_id] += 1
        else:
            cart_items[product_id] = 1

    products = []
    total = 0
    for product_id, quantity in cart_items.items():
        product = Product.query.get(product_id)
        product.quantity = quantity
        products.append(product)
        total += product.price * quantity

    return render_template('cart.html', products=products, total=total)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not current_user.is_authenticated:
        flash('Please login to checkout', 'warning')
        return redirect(url_for('login'))

    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('index'))

    # Calculate total
    cart_items = {}
    for product_id in session['cart']:
        if product_id in cart_items:
            cart_items[product_id] += 1
        else:
            cart_items[product_id] = 1

    line_items = []
    for product_id, quantity in cart_items.items():
        product = Product.query.get(product_id)
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': product.price,
            },
            'quantity': quantity,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('cancel', _external=True),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash('Something went wrong with payment processing', 'danger')
        return redirect(url_for('cart'))


@app.route('/success')
def success():
    session_id = request.args.get('session_id')

    try:
        # Retrieve the Stripe session
        checkout_session = stripe.checkout.Session.retrieve(session_id)

        # Create order record
        order = Order(
            user_id=current_user.id,
            stripe_id=checkout_session.payment_intent,
            amount=checkout_session.amount_total,
            status='paid'
        )
        db.session.add(order)

        # Add order items
        cart_items = {}
        for product_id in session['cart']:
            if product_id in cart_items:
                cart_items[product_id] += 1
            else:
                cart_items[product_id] = 1

        for product_id, quantity in cart_items.items():
            order_item = OrderItem(
                order_id=order.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(order_item)

        db.session.commit()

        # Clear cart
        session.pop('cart', None)

        return render_template('success.html')
    except Exception as e:
        flash('Error processing your order', 'danger')
        return redirect(url_for('index'))


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


@app.route('/account')
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.id.desc()).all()
    return render_template('account.html', orders=orders)


@app.route('/order/<int:order_id>')
def order(order_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)

    return render_template('order.html', order=order)


if __name__ == "__main__":
    app.run(debug=True)