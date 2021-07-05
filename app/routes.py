from app import app
from flask import jsonify, render_template
""" 
CREATE - POST
READ - GET
UPDATE - PUT
DELETE - DELETE
"""

@app.route('/users')
def get_users():
    return jsonify({'message': 'This works!'})

@app.route('/profile')
def profile():
    logged_in_user = 'Rachel'
    return render_template('profile.html', u=logged_in_user)

@app.route('/blog')
def blog():
    return 'This where you blog'

@app.route('/contact')
def contact():
   return 'This is where contact info would be.'
