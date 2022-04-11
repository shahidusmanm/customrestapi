import os
import pymysql
from flask import jsonify, request
import secrets
import hashlib

# initialising database details
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# function to allow for connection to the SQL database
def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    conn = pymysql.connect(user="cloudcomputing", password="cloudcomputing", db=db_name, host='35.246.95.43', cursorclass=pymysql.cursors.DictCursor)
    return conn

'''Users CRUD'''

# CREATE function to add a user
def add_user(user):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO cloudcomputingtask.tbl_users (user_created_datetime, username,user_email, user_fname, user_lname, user_md5_pass, role) VALUES(NOW(),%s, %s, %s,%s, %s, "admin")',
        (user['username'],user["user_email"],user["user_fname"], user["user_lname"], hashlib.md5(user["user_password"].encode('utf-8')).hexdigest()))
    conn.commit()
    conn.close()

# READ function to see all users
def get_users():
    conn = open_connection()
    with conn.cursor() as cursor:

        # If task_id has not been specified, read all of a user's tasks
        result = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_users')
        tasks = cursor.fetchall()
        if result > 0:
            answer = tasks
        else:
            answer = 'No user found'
    conn.close()
    return answer

# UPDATE function to change user's email
def update_user(user):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('UPDATE cloudcomputingtask.tbl_users SET user_email = %s WHERE user_id = %s', (user["new_email"], user["user_id"]))
    conn.commit()
    conn.close()

# DELETE function to delete a user by id
def del_user(username):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('DELETE FROM cloudcomputingtask.tbl_users WHERE (username) = (%s)', (username))
    conn.commit()
    conn.close()

# READ function to see single user
def get_user(name):
    conn = open_connection()
    with conn.cursor() as cursor:

        # If task_id has not been specified, read all of a user's tasks
        result = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_users WHERE username = %s', (name))
        tasks = cursor.fetchall()
        if result > 0:
            answer = tasks
        else:
            answer = 'No user found'
    conn.close()
    return answer
