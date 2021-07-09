from .import bp as app
from flask import render_template, request, url_for, flash, redirect
from flask_login import current_user
from app import db
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post


@app.route('/')
def home():
    context = {
        'posts': current_user.followed_posts() if current_user.is_authenticated else []
    }
    return render_template('home.html', **context)

@app.route('/', methods=['GET', 'POST'] )
def create_post():
    if request.method =='POST':
        post =Post(body=request.form.get('body_text'), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('You added a new post!', 'success')
        return render_template('home.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        print(request.form.get('first_name'))
        print(request.form.get('last_name'))
        print(request.form.get('email'))

        u = User.query.get(current_user.id)
        u.first_name = request.form.get('first_name')
        u.last_name = request.form.get('last_name')
        u.email = request.form.get('email')
        db.session.commit()
        flash('Profile updated successfully', 'info')
        return redirect(url_for('main.profile'))
    context = {
            'posts': current_user.own_posts()
        }

    return render_template('profile.html', **context)
        

@app.route('/contact')
def contact():
   return 'This is where contact info would be.'