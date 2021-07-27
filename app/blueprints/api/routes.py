from flask.json import jsonify
from .import bp as api
from flask import current_app
from app.blueprints.blog.models import Post
from flask_login import current_user
import stripe 

@api.route('/blog/')
def get_posts():
    """
    [GET] /api/blog
    """
    # post = Post.query.all()
    return jsonify({ p.to_dict() for p in Post.query.all()})

@api.route('/blog/user/post')
def get_user_posts():
    """
    [GET] /api/blog/user
    """
    # post = Post.query.all()
    return jsonify([p.to_dict() for p in current_user.posts.all()])

# STRIPE PRODUCT ROUTES
@api.route('/shop/products')
def get_products():
    stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')
    return jsonify(stripe.Product.list())
