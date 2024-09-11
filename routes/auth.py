from flask import Blueprint, request, jsonify
from models import *
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
import datetime

bp = Blueprint('auth', __name__)

@bp.route("/register", methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    user = User(username=username, password=hashed_password, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created!"})

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    if user is None:
        return jsonify({"error": "User not found!"}), 401
    
    if bcrypt.checkpw(str.encode(password), user.password):
        access_token = create_access_token(identity=username, additional_claims={"user_id": user.id}, expires_delta=datetime.timedelta(hours=1))
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid credentials"}), 401


@bp.route('/user-info', methods=['GET'])
@jwt_required()
def get_user_info():
    claims = get_jwt()
    user_id = claims['user_id']

    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })