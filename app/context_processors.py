from flask_login import current_user
from flask import current_app as app
from app.blueprints.shop.models import Cart, Product, StripeProduct
from functools import reduce

@app.context_processor
def build_cart():
    cart_dict = {}
    if current_user.is_anonymous:
        return {
            'cart_dict': cart_dict,
            'cart_size' : 0,
            'cart_subtotal': 0,
            'cart_tax': 0,
            'cart_grandtotal' : 0       
        }

    # Find the User's cart
    cart = Cart.query.filter_by(user_id=current_user.id).all()
    if len(cart) > 0:
        # loop through the cart
        for cart_item in cart:
            p =StripeProduct.query.filter_by(stripe_product_id=cart_item.product).first()
            if cart_item.product not in cart_dict:
                cart_dict[p.stripe_product_id] = {
                    'id': cart_item.id,
                    'product_id': p.id,
                    'image': p.image,
                    'quantity': 1,
                    'name': p.name,
                    'description': p.description,
                    'price': p.price,
                    'tax' : p.tax
                }
            else:
                cart_dict[p.stripe_product_id]['quantity'] += 1

    def format_currency(price):
        return f'{price:,.2f}'

    return {
            'cart_dict': cart_dict,
            'cart_size': len(cart),
            'cart_subtotal': format_currency(float(reduce(lambda x,y:x+y, [i.to_dict()['product'].price for i in cart]))) if cart else 0,
            'cart_tax': format_currency(float(reduce(lambda x,y:x+y, [i.to_dict()['product'].tax for i in cart]))) if cart else 0,
            'cart_grandtotal': format_currency(float(reduce(lambda x,y:x+y, [i.to_dict()['product'].price + i.to_dict()['product'].tax for i in cart]))) if cart else 0
        }

@app.context_processor
def get_stripe_keys():
    return {
        'STRIPE_PUBLISHABLE_KEY': app.config.get('STRIPE_PUBLISHABLE_KEY')
        }