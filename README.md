#This is Task Management App created by Mayank Nagariya.

Tech stack used-
1. Backend- Flask (choosen flask because it's very lightweight and gives us flexibility to choose other things)
2. DB- sqlite (we needed lightweighted database, so choosen inbuilt sqlite, there is no need to use external DBs)


# run below command to install dependecies-

pip install -r requirements.txt 

# for jwt secret key-
create .env file in folder. 
JWT_SECRET_KEY = <keep any secret string key>
e.g- JWT_SECRET_KEY = "TWSproject"

# for db setup use below commands -

flask db init 
flask db migrate -m "initail database setup"
flask db upgrade 

# run flask app using either of the below commands -
python app.py
flask run 
or use vs code debug mode to run app. 

# Now open postman for checking api run in post method 127.0.0.1:5000/user/ 
-by this format you can create a user 
{
    "username": "<username>",
    "password": "<password>"
}

# Now run 127.0.0.1:5000/user/login for login/get access token 
-by this format you login or get access token 
{
    "username": "<username>",
    "password": "<password>"
}

# Now run 127.0.0.1:5000/task/ for creating a task
-by using this format you can create a task

{
    "title": "<title>",
    "description": "<desccription>",
    "due_date": "<due_date>",
    "members": [<associated_members_id>]
}

# Now run 127.0.0.1:5000/task/read for fetching/reading a task by a user
-you can also give 'task_id' in query param (eg- http://127.0.0.1:5000/task/read?task_id=1) for fetching a specific task

# Now run 127.0.0.1:5000/task/update for updating a task
-by this format you can update any column of a particular task you can also change "status" of a particular task

{
    "task_id": 8,  **(must)
    "title": "<new_title>",
    "description":"<new_description>",
    "status": "<TODO/IN-PROGRESS/DONE>",
    "due_date": "<new_due_date>"
}

# Now run 127.0.0.1:5000/task/member for adding or removing member from a particular task
-by using this format you can add/remove associated members from a particular task

{
    "add": [<members_id>],
    "remove": [<members_id>],
    "task_id": 12 **(must)
}

# Now run 127.0.0.1:5000/task/member/view for viewing  members associated with a particular task
-you have to give "task_id" in query param (eg- http://127.0.0.1:5000/task/read?task_id=1) of which you want to fetch "associated_members" list

# Now run 127.0.0.1:5000/task/delete/<int:task_id> for deleting a task
-you have to give "task_id" in path param (eg- http://127.0.0.1:5000/task/delete/1) for deleting a task
