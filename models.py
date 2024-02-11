from db_connection import db 
from enum import Enum

class User(db.Model):

    __tablename__="user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class StatusEnum(Enum):
    TODO = 'TODO'
    INPROGRESS = 'IN-PROGRESS'
    DONE = 'DONE'

class Task(db.Model):

    __tablename__="task"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    due_date=db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.TODO)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class TaskUser(db.Model):

    __tablename__ = "task_user_mapping"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    
