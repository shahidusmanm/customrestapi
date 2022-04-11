# importing of neccessary modules and functions
from flask import Flask, request, jsonify
from db_users import *
from db_tasks import *
from authentication import *

# initialising instance
app = Flask(__name__)

# Defining the login
@app.route('/login', methods=['POST'])
def user_login():
    #This function will need an api_key to return
    email = request.get_json()['user_email']
    password = request.get_json()['user_password']
    session_key = login (email, password)
    return jsonify(session_key)
@app.route('/auth', methods=['POST'])
def user_auth():
    #This function will need an api_key to return
    session_key = request.get_json()['session_key']
    isAuthorized = auth (session_key)
    return jsonify(isAuthorized)


'''TASKS CRUD'''

# READ all tasks
@app.route('/view/tasks', methods=['POST'])
def view_tasks():
    # Authentication via key/db_password
    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # Creating a new task in the database
    if isAuthorized == True:
        if all (k in request_json for k in ("username", "user_api_key")):
            # call create function
            task_id = 0
            task_list = get_user_tasks (request_json['username'], task_id)
            return jsonify(task_list), 200
        else:
            return jsonify("Your request body is missing parameters. Required parameters are Username."), 400

# READ a single task defined by the ID
@app.route('/view/task/<task_id>', methods=['POST'])
def view_task(task_id):
    # Authentication via key/db_password
    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # Creating a new task in the database
    if isAuthorized == True:
        if all (k in request_json for k in ("username", "user_api_key")):
            # call create function
            task_list = get_user_tasks (request_json['username'], task_id)
            return jsonify(task_list), 200
        else:
            return jsonify("Your request body is missing parameters. Required parameters are Username."), 400

# CREATE a task
@app.route('/create/task', methods=['POST'])
def create_tasks():
    # Authentication via key/db_password
    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # Creating a new task in the database
    if isAuthorized == True:
        if all (k in request_json for k in ("task_title","task_description", "username")): #task_status
            # call create function
            task_id = create_user_tasks (request_json['username'], request_json['task_title'], request_json['task_description'])
            result = "Your task has been created. Your Task ID is: " + str(task_id)
            return jsonify(result), 200
        else:
            return jsonify("Your request body is missing parameters. Required parameters are Username, Title and Description"), 400

# UPDATE a task
@app.route('/update/task/<task_id>', methods=['PUT'])
def update_tasks (task_id):

    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])
    title = desc = "None"
    status = 5

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    if isAuthorized:
        if all (k in request_json for k in ("username", "task_title")):
            result = update_user_tasks (request_json['username'], request_json['task_title'], desc, status, task_id)
            return result, 200
            #return jsonify("Your title has been updated"), 200

        if all (k in request_json for k in ("username", "task_description")):
            result = update_user_tasks (request_json['username'], title, request_json['task_description'], status, task_id)
            return result, 200
            #return jsonify("Your description has been updated"), 200

        if all (k in request_json for k in ("username", "task_status")):
            result = update_user_tasks (request_json['username'], title, desc, request_json['task_status'], task_id)
            return result, 200
            #return jsonify("Your status has been updated"), 200

        else:
            return jsonify("Your request body is missing parameters. Required parameters are Username. Optional parameters are Title, Description and Status"), 400

# DELETE a task
@app.route('/delete/task/<taskid>', methods=['DELETE'])
def delete_tasks (taskid):

    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # Creating a new task in the database
    if isAuthorized == True:
        delete_user_tasks (request_json["username"], taskid)
        return jsonify("Your task has been deleted"), 200


'''USERS CRUD'''

# READ all users 
@app.route('/view/users', methods=['POST'])
def view_users():
    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])
    isAdmin = admin(request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # Reading a single user's details
    if isAuthorized == True:
        if isAdmin:
            user = get_users()
            return jsonify(user), 200
        else:
            return jsonify("Unauthorized: Admin privileges needed"), 401

# READ single user 
@app.route('/view/user/<username>', methods=['POST'])
def view_user(name):
    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])
    isAdmin = admin(request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # Reading a single user's details
    if isAuthorized == True:
        if isAdmin:
            if all (k in request_json for k in ("username", "user_api_key")):
                # call create function
                user = get_user(name)
                return jsonify(user), 200
            else:
                return jsonify("Your request body is missing parameters. Required parameters are Username and api-key."), 400
        else:
            return jsonify("Unauthorized: Admin privileges needed"), 401

# CREATE user
@app.route('/create/user', methods = ['POST'])
def create_user():
    request_json = request.get_json()
    if all (k in request_json for k in ("user_fname", "user_lname", "username", "user_password", "user_email")):
        user = add_user(request_json)
        return jsonify('User created'), 200
    else:
        return jsonify("Your request body is missing parameters. Required parameters are user_fname, user_lname, username, password, user_email"), 400


# DELETE user 
@app.route('/delete/user/<username>', methods=['DELETE'])
def delete_user(username):
    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])
    isAdmin = admin(request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # check
    if isAuthorized == True:
        if isAdmin:
            if all (k in request_json for k in ("username", "user_api_key")):
                del_user(username)
                return jsonify('User Deleted'), 200
            else:
                return jsonify('Your request body is missing parameters. '), 400
        else:
            return jsonify("Unauthorized: Admin privileges needed"), 401

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
