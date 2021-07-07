from flask import render_template, url_for, jsonify
from .import bp as app

posts = [
    {
        'id': 1,
        'body': 'This is the first blog post.',
        'author': 'Lucas L.',
        'timestamp': '10-2-2020'
        },
    {
        'id': 2,
        'body': 'This is the second blog post.',
        'author': 'Derek H.' ,
        'timestamp': '10-3-2020'
        },        
    {
        'id': 3,
        'body': 'This is the third blog post.',
        'author': 'Joel C.',
        'timestamp': '10-4-2020'
        }    
    ]


@app.route('/')
def home():
    context = {
        'posts': posts
    }
    return render_template('home.html', **context)

@app.route('/profile')
def profile():
    logged_in_user = 'Rachel'
    return render_template('profile.html', u=logged_in_user)

@app.route('/contact')
def contact():
   return 'This is where contact info would be.'