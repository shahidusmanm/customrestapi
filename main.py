from flask import Flask, request, jsonify
from db_users import *
from db_tasks import *
from authentication import *

app = Flask(__name__)

'''TASKS TABLE'''


## Done
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


## Done
@app.route('/test', methods=['POST'])
def test():
    #This function will need an api_key to return
    email = request.get_json()['user_email']
    output = test_db_function (email)
    return output


@app.route('/tasks', methods=['GET'])
def tasks():
    #This function will need an api_key to return
    if request.method == 'GET':
        #request.headers['api_key']
        # You pass the http request alone
        return get_tasks()
    else:
        return 'error', 404

## Done
# View all tasks
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

## Done
# View a single task defined by the ID
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


## Done
# create a single task
@app.route('/create/task', methods=['POST'])
def create_tasks():
    # Authentication via key/db_password
    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # Creating a new task in the database
    if isAuthorized == True:
        if all (k in request_json for k in ("task_title","task_description", "task_status", "username")):
            # call create function
            task_id = create_user_tasks (request_json['username'], request_json['task_title'], request_json['task_description'], request_json['task_status'])
            result = "Your task has been created. Your Task ID is: " + str(task_id)
            return jsonify(result), 200
        else:
            return jsonify("Your request body is missing parameters. Required parameters are Username, Title, Description and Status"), 400

## Done
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
            return result
            #return jsonify("Your title has been updated"), 200

        if all (k in request_json for k in ("username", "task_description")):
            result = update_user_tasks (request_json['username'], title, request_json['task_description'], status, task_id)
            return result
            #return jsonify("Your description has been updated"), 200

        if all (k in request_json for k in ("username", "task_status")):
            result = update_user_tasks (request_json['username'], title, desc, request_json['task_status'], task_id)
            return result
            #return jsonify("Your status has been updated"), 200

        else:
            return jsonify("Your request body is missing parameters. Required parameters are Username. Optional parameters are Title, Description and Status"), 400

## Done
@app.route('/task/<taskid>', methods=['DELETE'])
def delete_tasks (taskid):

    request_json = request.get_json()
    isAuthorized = auth (request_json['user_api_key'])

    if isAuthorized == False:
        return jsonify("Unauthorized: You don't have permission to view this resouce"), 401

    # Creating a new task in the database
    if isAuthorized == True:
        delete_user_tasks (request_json["username"], taskid)
        return jsonify("Your task has been deleted"), 200


'''USERS TABLE'''

# READ all users + CREATE user + UPDATE user's email
@app.route('/users', methods=['GET', 'POST', 'PUT'])
def users():
    isAuthorized = auth (request.get_json()['user_api_key'])

    if request.method == 'GET':
        # You pass the http request alone
        return get_users()
    elif request.method == 'POST':
        # You pass a json with: user["user_email"],user["user_fname"],user["user_lname"],user["user_password"]
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        add_user(request.get_json())
        return 'User Added'
    elif request.method == 'PUT':
        # You pass a json with: user["new_email"], user["user_id"]
        if not request.is_json:
            return jsonify({"msg: Missing JSON in request"}), 400
        update_user(request.get_json())
        return "User's Email Updated"
    else:
        return 'error', 404

# READ single user
@app.route('/users/<name>', methods=['GET'])
def user(name):
    isAuthorized = auth (request.get_json()['user_api_key'])
    if request.method == 'GET':
        # You pass a http request with: first_name last_name
        return get_user(name)
    else:
        return 'error', 404

# DELETE user
@app.route('/delete/<userid>', methods=['DELETE'])
def delete(userid):

    if request.method == 'DELETE':
        # You pass a http request with: user_id
        del_user(userid)
        return 'User deleted'
    else:
        return 'error', 404


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
