from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import *

bp = Blueprint("tasks", __name__)

@bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_tasks():
    claims = get_jwt()

    user_id = claims["user_id"]

    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    newTask = Task(title=title, description=description, user_id=user_id, status=status)

    db.session.add(newTask)
    db.session.commit()

    return { "message": "Task created" }, 201

@bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    claims = get_jwt()
    user_id = claims["user_id"]

    user = User.query.get(user_id)

    tasks = Task.query.filter_by(user_id=user_id).all()

    task_list = [{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "status": t.status
    } for t in tasks]

    return jsonify(task_list), 200

@bp.route("/tasks", methods=["POST"])
@jwt_required()
def edit_task(task_id):
    claims = get_jwt

    user = claims["user_id"]

    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    target_task = Task.query.get(task_id)
    if not target_task:
        return jsonify({"msg": "Task not found"}), 404

    if title is not None:
        target_task.title = title

    if description is not None:
        target_task.description = description

    if status is not None:
        target_task.status = status

    db.session.commit()

    return jsonify({"msg": "Task Updated", "task_id": target_task.id}), 200




bp.route("/tasks", method=["POST"])
@jwt_required()

def remove_tasks(task_id):
    claims = get_jwt()
    user = claims["user_id"]

    task = Task.query.get(task_id)
    if not Task:
        return jsonify({"msg": "Task not found"}), 404
    
    if task.user_id != user:
        return jsonify({"msg": "Unauthorized"}), 403
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"msg": "Task deleted"}), 200




