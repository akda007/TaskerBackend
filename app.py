from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from models import *
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_secret_key')

CORS(app)
jwt = JWTManager(app)
migration = Migrate(app, db)

db.init_app(app)

from routes import auth, tasks, groups

app.register_blueprint(auth.bp)
app.register_blueprint(tasks.bp)
app.register_blueprint(groups.bp)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
