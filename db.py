import os
import pymysql
from flask import jsonify, request
import secrets
import hashlib

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# function to allow for connection to the SQL database
def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    conn = pymysql.connect(user=db_user, password=db_password, db=db_name, host='35.246.95.43', cursorclass=pymysql.cursors.DictCursor)
    return conn

'''Tasks CRUD'''

# READ function to see all tasks
def get_tasks():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM cloudcomputingtask.tbl_tasks')
        tasks = cursor.fetchall()
        if result > 0:
            answer = jsonify(tasks)
        else:
            answer = 'No Active Tasks Found'
    conn.close()
    return answer

# CREATE function to add a task
def add_task(task):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO cloudcomputingtask.tbl_tasks (user_api_key,user_created_datetime,user_email, user_fname, user_lname, user_password, user_md5_pass) VALUES(%s,NOW(),%s, %s, %s,%s, %s)', 
        (secrets.token_urlsafe(10),user["user_email"],user["user_fname"], user["user_lname"], user["user_password"], hashlib.md5(user["user_password"].encode('utf-8'))))
    conn.commit()
    conn.close()



'''Users CRUD'''

# CREATE function to add a user
def add_user(user):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO cloudcomputingtask.tbl_users (user_api_key,user_created_datetime,user_email, user_fname, user_lname, user_password, user_md5_pass) VALUES(%s,NOW(),%s, %s, %s,%s, %s)', 
        (secrets.token_urlsafe(10),user["user_email"],user["user_fname"], user["user_lname"], user["user_password"], hashlib.md5(user["user_password"].encode('utf-8'))))
    conn.commit()
    conn.close()

# READ function to see all users
def get_users():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM cloudcomputingtask.tbl_users')
        users= cursor.fetchall()
        if result > 0:
            answer = jsonify(users)
        else:
            answer = 'No Users Found'
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
def del_user(userid):
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('DELETE FROM cloudcomputingtask.tbl_users WHERE (user_id) = (%s)', (userid))
    conn.commit()
    conn.close()

# READ function to see single user
def get_user(name):
    conn = open_connection()
    first_name, last_name = name.split(' ')
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM cloudcomputingtask.tbl_users WHERE user_fname = %s AND user_lname=%s',
        (first_name, last_name))
        user = cursor.fetchall()
        if result > 0:
            answer = jsonify(user)
        else:
            answer = 'No Users Found'
    conn.close()
    return answer