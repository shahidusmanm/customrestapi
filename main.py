from flask import Flask, request, jsonify
from db_users import *
from db_tasks import *
from authentication import *

app = Flask(__name__)

'''TASKS TABLE'''

# READ all tasks
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


@app.route('/view/tasks', methods=['POST'])
def view_tasks():
    # Authentication via key/db_password
    isAuthorized = auth (request.get_json()['user_api_key'], request.get_json()['user_email'], request.get_json()['user_password'])

    if isAuthorized == False:
        return jsonify({"msg: Unauthorized: You don't have permission to view this resouce"}), 401

    # Creating a new task in the database
    if isAuthorized == True:
        tasks = get_user_tasks (request.get_json())
        return tasks

    return jsonify({"msg: Your request body is missing parameters"}), 400


@app.route('/tasks', methods=['POST'])
def create_tasks():
    # Authentication via key/db_password
    isAuthorized = auth (request.get_json()['user_api_key'], request.get_json()['user_email'], request.get_json()['user_password'])

    if isAuthorized == False:
        return jsonify({"msg: Unauthorized: You don't have permission to view this resouce"}), 401

    # Creating a new task in the database
    if isAuthorized == True:
        create_user_tasks (request.get_json())
        return jsonify({"msg: Your task has been created"}), 200

    return jsonify({"msg: Your request body is missing parameters"}), 400


@app.route('/tasks/<taskid>', methods=['PUT'])
def update_tasks (taskid):
    isAuthorized = auth (request.get_json()['user_api_key'], request.get_json()['user_email'], request.get_json()['user_password'])
    if isAuthorized == False:
        return jsonify({"msg: Unauthorized: You don't have permission to perform this action"}), 401

    if isAuthorized:
        update_user_tasks (request.get_json(), taskid)
        return jsonify({"msg: Your task has been updated"}), 200


@app.route('/tasks/<taskid>', methods=['DELETE'])
def delete_tasks (taskid):
    isAuthorized = auth (request.get_json()['user_api_key'], request.get_json()['user_email'], request.get_json()['user_password'])
    if isAuthorized == False:
        return jsonify({"msg: Unauthorized: You don't have permission to perform this action"}), 200

    if isAuthorized:
        delete_user_tasks (request.get_json(), taskid)
        return jsonify({"msg: Your task has been deleted"}), 401


'''USERS TABLE'''

# READ all users + CREATE user + UPDATE user's email
@app.route('/users', methods=['GET', 'POST', 'PUT'])
def users():
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
