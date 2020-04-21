from flask import Flask

from app.models import db, migrate
from app.routes.home_routes import home_routes
from app.routes.book_routes import book_routes

DATABASE_URI = "sqlite:////Users/mjr/Desktop/twitoff-13/twitoff_13.db" # TODO: read from env var
SECRET_KEY = "super secret" # TODO: read from env var

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY # required for flash messaging

    # configure the database:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # suppress warning messages
    db.init_app(app)
    migrate.init_app(app, db)

    # configure routes:
    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
