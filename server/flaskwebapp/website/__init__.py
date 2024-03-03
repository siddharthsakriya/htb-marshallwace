from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "recycled.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdpgroup13'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import User
    from .routes import routes

    app.register_blueprint(routes, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app

def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
