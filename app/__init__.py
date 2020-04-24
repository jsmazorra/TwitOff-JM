from flask import Flask
from app.models import db, migrate
from app.routes.home_routes import home_routes
from app.routes.book_routes import book_routes

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", default="super secret")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY # required for flash messaging

    # configure the database:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # suppress warning messages
    db.init_app(app)
    migrate.init_app(app, db)

    # configure routes:
    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(tweets_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(stats_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
