from flask import render_template, url_for, request, redirect, flash 
from app.blueprints.blog.models import Post
from .import bp as app
from flask_login import current_user, login_required
from app import db

@app.route('/post/<int:id>')
@login_required
def get_post(id):
    context = {
        'p': Post.query.get(id)
    }
    return render_template('blog-single.html', **context)

# Derek functionality for creating post
# @app.route('/post/create', method=['POST'])
# def create_post():
#     Post(body=request.form.get('body'),user_id=current_user).save()
#     flash('Post created successfully.')
#     return redirect(url_for('main.home'))