from flask import jsonify,Response,request
from http import HTTPStatus
from models import User,Task,TaskUser
from datetime import datetime
from db_connection import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token)


def login_service(username, password):
    
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        
        access_token = create_access_token(identity=username, additional_claims={
            'user_id': user.id
        })
        refresh_token = create_refresh_token(identity=username, additional_claims={
            'user_id': user.id
        })

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, HTTPStatus.OK.value
    else:
        
        return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED.value



def add_user_service(data):
    hashed_password = generate_password_hash(data["password"], method='pbkdf2:sha256')
    adduser=User(username=data["username"],password=hashed_password)
    db.session.add(adduser)
    db.session.commit()
   
    return jsonify({"message":"user added sucessfully", "user_id":adduser.id})


def create_task_service(data,user_id):
    
    title=data["title"]
    description=data["description"]
    members=data["members"]
    due_date_str=data["due_date"]
    due_date = datetime.strptime(due_date_str, "%d-%m-%Y").date()

    addtask=Task(title=title, description=description,due_date=due_date,user_id=user_id)
    db.session.add(addtask)
    db.session.flush()
    task_id=addtask.id
    for member in members:
        addmember=TaskUser(task_id=task_id,user_id=member)
        db.session.add(addmember)
    
    db.session.commit()
    return jsonify({"message":"task added sucessfully", "task_id":task_id})

def read_task_service(task_id,user_id):
    tasks=db.session.query(Task.id,Task.title,Task.description,
                             Task.status,Task.due_date,
                             func.group_concat(TaskUser.user_id.distinct())\
                            .label("associate_member")).join(
                            TaskUser,Task.id==TaskUser.task_id)\
                            .filter(Task.user_id==user_id).group_by(
                            Task.id,Task.title,Task.description,
                            Task.status,Task.due_date)

    if task_id:
        tasks=tasks.filter(Task.id==task_id)

    tasks=tasks.all()
    response=[]
    for task in tasks:
        info=dict(task_id=task.id,title=task.title,
                  description=task.description,
                  due_date=task.due_date,status=task.status.value,
                  associated_members=[int(i) for i in task.associate_member.split(",")])
        response.append(info)
        
    return response

def update_task_service(data):
    task_id=data.get("task_id")
    task=Task.query.get(task_id)
    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    new_title=data.get("title") if "title" in data else task.title
    new_description=data.get("description") if "description" in data else task.description
    new_due_date_str=data.get("due_date") 
    new_due_date=datetime.strptime(new_due_date_str, "%d-%m-%Y").date()\
                    if new_due_date_str else task.due_date
    new_status=data.get("status") if "status" in data else task.status


    task.title = new_title 
    task.description=new_description
    task.due_date=new_due_date
    task.status=new_status
    db.session.commit()

    return jsonify({"message":"task updated"})

def update_task_member_service(data):
    task_id=data["task_id"]
    if "add" in data:
        add=data["add"]
        for member in add:
            addmember=TaskUser(task_id=task_id,user_id=member)
            db.session.add(addmember)
            db.session.commit()
    if "remove" in data:
        remove=data["remove"]
        for member in remove:
            task = TaskUser.query.filter_by(task_id=task_id, user_id=member).first()
            db.session.delete(task)
            db.session.commit()

    return jsonify({"message":"member added/removed sucessfully"})

def view_task_member_service(task_id):
    member_list=db.session.query(TaskUser.user_id).filter(TaskUser.task_id==task_id)\
                                .group_by(TaskUser.user_id).all()
    response=[i[0] for i in member_list]
    return jsonify({"associate_members":response})



def deleting_task_service(task_id):
    task = Task.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': f'Task {task_id} deleted successfully'})
    else:
        return jsonify({'message': f'Task {task_id} not found'}), 404
