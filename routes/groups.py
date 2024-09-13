
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

@bp.route("/groups/<int:group_id>", methods=["DELETE"])
@jwt_required()
def delete_groups(group_id):
    group = Group.query.get(group_id)

    if not group:
        return jsonify({"msg": "Group not found"}), 404

    db.session.delete(group)
    db.session.commit()

    return jsonify({"msg": "Group deleted"}), 200


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



@bp.route("/groups/<int:group_id>/tasks", methods = ["POST"])
@jwt_required()
def add_task_to_group(group_id):
    claims = get_jwt()
    user_id = claims["user_id"]

    data = request.get_json()
    
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    group = Group.query.get(group_id)

    if not group_id:
        return jsonify({"msg": "Group not found"}), 404
    
    user = User.query.get(user_id)
    if group not in user.groups:
        return jsonify({"msg": "Permission denied"}), 403
    
    new_task = Task(title = title, description = description, status = status, group_id = group_id)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"msg": "Task created", "task_id": new_task.id}), 201


@bp.route("/groups/<int:group_id>/tasks", methods=["GET"])
@jwt_required()
def get_group_tasks(group_id):
    claims = get_jwt()
    user_id = claims["user_id"]

    status = request.args.get("status", None)

    group = Group.query.get(group_id)

    if not group:
        return jsonify({"msg": "Group not found"}), 404

    if status:
        tasks = Task.query.filter_by(group_id=group_id, status=status).all()
    else:
        tasks = Task.query.filter_by(group_id=group_id).all()

    task_list = [{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "status": t.status
    } for t in tasks]

    return jsonify(task_list), 200


@bp.route("/groups/<int:group_id>/tasks/<int:task_id>", methods=["POST"])
@jwt_required()
def edit_group_tasks(group_id, task_id):
    claims = get_jwt()
    user = claims["user_id"]

    data = request.get_json()
    
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    target_task = Task.query.get(task_id)
    if not target_task:
        return jsonify({"msg": "Task not found"}), 404

    group = Group.query.get(group_id)
    if not group:
        return jsonify({"msg": "Groups not found"}), 404
    
    if target_task.group != group:
        return jsonify({"msg": "Taks does not belong to this group"}), 404

    if title is not None:
        target_task.title = title

    if description is not None:
        target_task.description = description

    if status is not None:
        target_task.status = status

    db.session.commit()

    return jsonify({"msg": "Task Updated", "task_id": target_task.id}), 200

