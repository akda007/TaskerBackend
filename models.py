from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

    groups = db.relationship('Group', secondary=user_group, back_populates='users')
    
    tasks = db.relationship('Task', backref='user', lazy=True)

class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), unique=True, nullable=False)
    
    users = db.relationship('User', secondary=user_group, back_populates='groups')
    
    tasks = db.relationship('Task', backref='group', lazy=True)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(Enum("pending", "active", "finished", name="status_enum", default="pending"))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
