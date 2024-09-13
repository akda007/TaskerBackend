from flask import Blueprint, request, jsonify
from sqlalchemy.util.langhelpers import repr_tuple_names

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

@bp.route("/user", methods=['PATCH'])
@jwt_required()
def update_user():
    claims = get_jwt()
    user_id = claims['user_id']

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')

    user = User.query.get(user_id)

    if username is not None and username != "" and username != user.username:
        check_username = user.query.filter_by(username=username).first()

        if check_username is not None:
            return jsonify({"msg": "username already exists!"}), 400

        user.username = username

    if email is not None and email != "" and email != user.email:
        check_email = user.query.filter_by(email=email).first()

        if check_email is not None:
            return jsonify({"msg": "email already exists!"}), 400

        user.email = email

    db.session.commit()

    access_token = create_access_token(identity=username,
                                       additional_claims={"user_id": user.id, "user_email": user.email},
                                       expires_delta=datetime.timedelta(hours=24))

    return jsonify({"msg": "User updated!", "token": access_token}), 200



@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    
    if user is None:
        return jsonify({"error": "User not found!"}), 401
    
    if bcrypt.checkpw(str.encode(password), user.password):
        access_token = create_access_token(identity=username, additional_claims={"user_id": user.id, "user_email": user.email}, expires_delta=datetime.timedelta(hours=24))
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

@bp.route("/users", methods=['GET'])
@jwt_required()
def find_users():
    username_query = request.args.get('username', '')
    exclude_group = request.args.get('exclude_group', None)

    query = User.query

    if username_query:
        query = query.filter(User.username.like(f"%{username_query}%"))

    if exclude_group:
        query = query.filter(~User.groups.any())

    users = query.all()

    user_list = [
        {
            "username": u.username
        } for u in users
    ]

    return jsonify(user_list)
