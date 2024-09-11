from venv import create

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from models import *

bp = Blueprint("groups", __name__)

@bp.route("/groups", methods=["GET"])
@jwt_required()
def get_groups():
    claims = get_jwt()
    user_id = claims["user_id"]

    user = User.query.get(user_id)
    groups = user.groups

    group_list = [
        {
            "id": group.id,
            "name": group.group_name
        } for group in groups
    ]

    return jsonify(group_list), 200

@bp.route("/groups", methods=["POST"])
@jwt_required()
def create_group():
    claims = get_jwt()
    user_id = claims["user_id"]

    data = request.get_json()
    name = data.get("name")

    user = User.query.get(user_id)

    new_group = Group(group_name=name)

    db.session.add(new_group)
    db.session.commit()

    user.groups.append(new_group)
    db.session.commit()

    return jsonify({
        "msg": "Group created!",
        "group_id": new_group.id
    }), 201



@bp.route("/groups/add", methods=["POST"])
@jwt_required()
def add_user_to_group():
    claims = get_jwt()
    user_id = claims.get("user_id")

    data = request.get_json()

    group_id = data.get("group_id")
    target_user = data.get("target_user")

    target = User.query.filter_by(username=target_user).first()
    group = Group.query.get(group_id)

    target.groups.append(group)

    db.session.commit()

    return jsonify({
        "msg": "User added to group!"
    }), 200