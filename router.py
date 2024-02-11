from flask import Blueprint,request,jsonify
from service import (add_user_service,create_task_service,login_service,
                     deleting_task_service,read_task_service,update_task_service,
                     update_task_member_service,view_task_member_service)
from flask_jwt_extended import (create_access_token,jwt_required, 
                                get_jwt_identity, get_jwt)

user_router=Blueprint("user",__name__)
task_router=Blueprint("task", __name__)

@user_router.post("/")
def add_user():
    data=request.get_json()

    return add_user_service(data)

@user_router.post('/login')
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    response, status_code = login_service(username, password)
    return jsonify(response), status_code

@user_router.post('/token/refresh')
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


@task_router.post("/")
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt()["user_id"]

    return create_task_service(data,user_id)

@task_router.get("/read")
@jwt_required()
def read_task():
    task_id = request.args.get("task_id")
    user_id = get_jwt()["user_id"]

    return read_task_service(task_id,user_id)

@task_router.post("/update")
@jwt_required()
def update_task():
    data=request.get_json()
    return update_task_service(data)

@task_router.post("/member")
@jwt_required()
def update_task_member():
    data=request.get_json()
    return update_task_member_service(data)

@task_router.get("/member/view")
@jwt_required()
def view_task_member():
    task_id=request.args.get("task_id")
    return view_task_member_service(task_id)

@task_router.get("/delete/<int:task_id>")
@jwt_required()
def delete_task(task_id):
    return deleting_task_service(task_id)

