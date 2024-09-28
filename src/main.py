import os
from flask import Flask
from init import db, ma, bcrypt, jwt

from src.controllers.auth_controller import auth_blueprint

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

    return app

if __name__ == "__main__":
    # Run the Flask app
    app = create_app()
    app.run(debug=True)