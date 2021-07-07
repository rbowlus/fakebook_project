from flask import render_template, url_for
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


@app.route('/post/<int:id>')
def get_post(id):
    for p in posts:
       if p['id'] == id:
           post = p
           break
    context = {
        'p': post
    }
    return render_template('blog-single.html', **context)
