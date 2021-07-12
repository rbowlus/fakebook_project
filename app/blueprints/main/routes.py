from werkzeug.utils import html
from .import bp as app
from flask import render_template, request, url_for, flash, redirect
from flask_login import current_user, login_required
from app import db, mail
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post
from flask_mail import Message


@app.route('/')
@login_required
def home():
    context = {
        'posts': current_user.followed_posts() if current_user.is_authenticated else []
    }
    return render_template('home.html', **context)

@app.route('/', methods=['GET', 'POST'] )
@login_required
def create_post():
    if request.method =='POST':
        post =Post(body=request.form.get('body_text'), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('You added a new post!', 'success')
        # return render_template('home.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        print(request.files.get('profile-image'))
        # print(request.form.get('first_name'))
        # print(request.form.get('last_name'))
        # print(request.form.get('email'))

        # u = User.query.get(current_user.id)
        # u.first_name = request.form.get('first_name')
        # u.last_name = request.form.get('last_name')
        # u.email = request.form.get('email')
        # db.session.commit()
        flash('Profile updated successfully', 'info')
        return redirect(url_for('main.profile'))
    context = {
            'posts': current_user.own_posts()
            # 'posts': Post.query.filter_by(current_user=user.id)
        }

    return render_template('profile.html', **context)
        

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email'),
            'inquiry':request.form.get('inquiry'),
            'message': request.form.get('message'),
        }
        msg = Message(
            'This is a Test Subject Line',
            sender='rachel.bowlus@gmail.com',
            reply_to=['from the form'],
            recipients=['rrbowlus@aol.com', 'rachel.bowlus@gmail.com'],
            html=render_template('email/contact-results.html', **form_data)
        )
        mail.send(msg)
        flash('Thank you for your message. We will get back to you within 48 hours.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html')