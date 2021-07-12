from flask.helpers import url_for
from .import bp as app
from flask import json, render_template, redirect, flash, request, session, current_app, jsonify
from .models import Product, Cart
from flask_login import current_user
import stripe 
from app import db

stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')

@app.route("/")
def index():
    """[GET] /shop"""
    context = {
        'products': Product.query.all()
    }
    return render_template('shop/index.html', **context)

@app.route('/cart')
def cart():
    """[GET] /shop/cart"""
    from app.context_processors import build_cart
    display_cart = build_cart()['cart_dict']
    session['session_display_cart'] = display_cart
    
    context = {
        'cart': display_cart.values()
    }

    if not current_user.is_authenticated:
        flash('You must login to view your cart' , 'warning')
        return redirect(url_for('authentication.login'))
    return render_template('shop/cart.html', **context)

@app.route('/cart/add')
def add_to_cart():
    """[GET] /shop/cart/add"""
    if not current_user.is_authenticated:
        flash('You must login to add items to cart' , 'warning')
        return redirect(url_for('authentication.login'))

    #Make a new product
    product = Product.query.get(request.args.get('id'))

    #Save it to cart
    Cart(user_id=current_user.id, product_id=product.id).save()
    flash(f'You have added {product.name} to the cart', 'success')
    return redirect(url_for('shop.index'))

@app.route('/shop/success')
def shop_success():
    pass

@app.route('/shop/failure')
def shop_failure():
    pass

@app.route('/checkout', methods=['POST'])
def checkout():
    dc = session.get('session_display_cart')

    l_items = []
    for product in dc.values():
        product_dict = {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product['name'],
                        # Does product['image'] need to be in []?
                        'image': product['image'],
                    },
                    ' unit_amount': int(float(product['price'])* 100),
                },
                'quantity': product['quantity'],
            }
        l_items.append(product_dict)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=l_items,
            mode='payment',
            success_url='http://localhoust:5000/shop/cart',
            cancel_url='http://localhoust:5000/shop/cart',
        )

        #Clear all items from cart
        [db.session.delete(i) for i in Cart.query.filter_by(user_id=current_user.id).all()]
        db.session.commit()

        flash('Your order  was processed successfully', 'primary')
        return jsonify({ 'session_id': checkout_session.id })
    except Exception as e:
        return jsonify(error=str(e)), 403
