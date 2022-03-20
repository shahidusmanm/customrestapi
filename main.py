from flask import Flask, request, jsonify
from db_users import *
from db_tasks import *

app = Flask(__name__)

'''TASKS TABLE'''

# READ all tasks
@app.route('/tasks', methods=['GET'])
def tasks():
    if request.method == 'GET':
        # You pass the http request alone
        return get_tasks()
    else:
        return 'error', 404


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
    app.run()
