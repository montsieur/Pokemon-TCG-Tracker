import os
from flask import Flask
from init import db, ma, bcrypt, jwt

from controllers.auth_controller import auth_blueprint
from controllers.cli_controller import cli_blueprint
from controllers.user_controller import user_blueprint
from controllers.cards_controller import card_blueprint
from controllers.set_controller import set_blueprint
from controllers.trading_controller import trading_blueprint
from controllers.wishlist_controller import wishlist_blueprint
from controllers.rarity_controller import rarity_blueprint
from controllers.status_controller import status_blueprint
from controllers.condition_controller import condition_blueprint

def create_app():
    # Create a Flask app
    app = Flask(__name__)

    # Configure the app (Database URL, JWT Secret, etc.)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://your_user:your_password@localhost/tcg_tracker')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    # Register blueprints (controllers)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(cli_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(card_blueprint)
    app.register_blueprint(set_blueprint)
    app.register_blueprint(trading_blueprint)
    app.register_blueprint(wishlist_blueprint)
    app.register_blueprint(rarity_blueprint)
    app.register_blueprint(status_blueprint)
    app.register_blueprint(condition_blueprint)

    return app

if __name__ == "__main__":
    # Run the Flask app
    app = create_app()
    app.run(debug=True)