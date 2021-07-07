from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.blueprints.blog import bp as blog
    app.register_blueprint(blog)

    from app.blueprints.main import bp as main
    app.register_blueprint(main)

    from app.blueprints.shop import bp as shop
    app.register_blueprint(shop)

    with app.app_context():
        #building the rest of flask application
        from .import routes

    return app