import os
import pymysql
from flask import jsonify, request
import secrets
import random
import hashlib

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

#Tasks CRUD

def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    conn = pymysql.connect(user="cloudcomputing", password="cloudcomputing", db=db_name, host='35.246.95.43', cursorclass=pymysql.cursors.DictCursor)
    return conn


def test_db_function(email):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT username FROM cloudcomputingtask.tbl_users WHERE user_email = %s', email)
        username = cursor.fetchall()
    conn.close()
    return jsonify(username)

# READ function to see user tasks
def get_user_tasks(username, task_id):

    conn = open_connection()
    with conn.cursor() as cursor:

        # If task_id has not been specified, read all of a user's tasks
        if task_id == 0:
            result = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_tasks WHERE username = %s', username)
            tasks = cursor.fetchall()
            if result > 0:
                answer = tasks
            else:
                answer = 'No Active Tasks Found'

        # If task_id has been specified, read the specified task
        else:
            result = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_tasks WHERE username = %s AND task_id = %s', (username, task_id))
            tasks = cursor.fetchall()
            if result > 0:
                answer = tasks
            else:
                answer = 'Incorrect Task ID'
    conn.close()
    return answer


def create_user_tasks(username, title, description, status):
    conn = open_connection()
    with conn.cursor() as cursor:
        task_id = random.getrandbits(16)
        cursor.execute('INSERT INTO cloudcomputingtask.tbl_tasks (user_api_key, task_id, username, task_title, task_description, task_status, task_created_datetime, task_updated_datetime) VALUES(%s, %s,%s, %s, %s, %s, NOW(), NOW())',
        ("00000",task_id, username, title, description, status))
    conn.commit()
    conn.close()
    return task_id

# UPDATE function that updates all fields that have been specified in the POST request
def update_user_tasks(username, title, description, status, task_id):
    conn = open_connection()
    with conn.cursor() as cursor:

        # Check if task_title has been sent in the request body and update the database if it has
        if title != 'None':
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_title = %s, task_updated_datetime = NOW() WHERE username = %s AND task_id = %s', (title, username, task_id))
            conn.commit()

        # Check if task_description has been sent in the request body and update the database if it has
        if description != "None":
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_description = %s, task_updated_datetime = NOW() WHERE username = %s AND task_id = %s', (description, username, task_id))
            conn.commit()

        # Check if task_status has been sent in the request body and update the database if it has
        if status != 5:
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_status = %s, task_updated_datetime = NOW() WHERE username = %s AND task_id = %s', (status, username, task_id))
            conn.commit()


    conn.close()
    return "Your task has been updated"

# DELETE function that deletes an entire row (or task) from the database
def delete_user_tasks(username, task_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM cloudcomputingtask.tbl_tasks WHERE username = %s AND task_id = %s', (username, task_id))
        conn.commit()
        conn.close()
    return 1
