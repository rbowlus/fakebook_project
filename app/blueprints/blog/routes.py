from flask import render_template, url_for, request, redirect, flash 
from app.blueprints.blog.models import Post
from .import bp as app
from flask_login import current_user
from app import db

@app.route('/post/<int:id>')
def get_post(id):
    context = {
        'p': Post.query.get(id)
    }
    return render_template('blog-single.html', **context)


