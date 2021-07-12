from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #Tell our Flask application to use SQLAlchemy, Migrate and LoginManager
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    moment.init_app(app)
    mail.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'authentication.login'
    login_manager.login_message= "You do  not have access to this page. Please login to continue."
    login_manager.login_message_category = 'danger'

    from app.blueprints.blog import bp as blog
    app.register_blueprint(blog)

    from app.blueprints.authentication import bp as authentication
    app.register_blueprint(authentication)

    with app.app_context():
        #building the rest of flask application (configurations, additional packages, etc)
        from app.blueprints.main import bp as main
        app.register_blueprint(main)

        from app.blueprints.shop import bp as shop
        app.register_blueprint(shop)
        
        from .import context_processors

    return app