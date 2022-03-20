import os
import pymysql
from flask import jsonify, request
import secrets
import hashlib

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

#Tasks CRUD

# READ function to see user tasks
def get_user_tasks(request_body):
    conn = open_connection()
    with conn.cursor() as cursor:

        cursor.execute('SELECT user_id FROM cloudcomputingtask.tbl_users WHERE user_email = ?', request_body['user_email'])
        user_id = int(cursor.fetchall())

        # If task_id has not been specified, read all of a user's tasks
        if task_id == 0:
            result = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_tasks WHERE user_id = ?', user_id)
            tasks = cursor.fetchall()
            if result > 0:
                answer = jsonify(tasks)
            else:
                answer = 'No Active Tasks Found'

        # If task_id has been specified, read the specified task
        else:
            result = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_tasks WHERE user_id = ? AND task_id = ?', (user_id, request_body['task_id']))
            tasks = cursor.fetchall()
            if result > 0:
                answer = jsonify(tasks)
            else:
                answer = 'Incorrect Task ID'
    conn.close()
    return answer


def create_user_tasks(request_body):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id FROM cloudcomputingtask.tbl_users WHERE user_email = ?', request_body['user_email'])
        user_id = int(cursor.fetchall())

        tasks = cursor.execute('SELECT task_id FROM cloudcomputingtask.tbl_tasks WHERE user_id = ?', user_id)
        task_id = int(cursor.fetchall())

        cursor.execute('INSERT INTO cloudcomputingtask.tbl_tasks (task_id, user_id, user_api_key, task_title, task_description, task_status, task_created_datetime, task_updated_datetime) VALUES(%s,%s, %s, %s,%s, %s, NOW(), NOW())',
        (secrets.token_urlsafe(5), user_id, request_body['user_api_key'], request_body["task_title"], request_body["task_description"], request_body["task_status"]))
        conn.commit()
        conn.close()
    return 0

# UPDATE function that updates all fields that have been specified in the POST request
def update_user_tasks(request_body):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id FROM cloudcomputingtask.tbl_users WHERE user_email = ?', request_body['user_email'])
        user_id = int(cursor.fetchall())

        # Check if task_title has been sent in the request body and update the database if it has
        if "task_title" in request_body:
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_title = ?, task_updated_datetime = NOW() WHERE user_id = ? AND task_id = ?', (request_body['task_title'], user_id, request_body['task_id']))

        # Check if task_description has been sent in the request body and update the database if it has
        if "task_description" in request_body:
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_description = ?, task_updated_datetime = NOW() WHERE user_id = ? AND task_id = ?', (request_body['task_description'], user_id, request_body['task_id']))

        # Check if task_status has been sent in the request body and update the database if it has
        if "task_status" in request_body:
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_status = ?, task_updated_datetime = NOW() WHERE user_id = ? AND task_id = ?', (request_body['task_status'], user_id, request_body['task_id']))
        conn.commit()
        conn.close()
    return 0

# DELETE function that deletes an entire row (or task) from the database
def delete_user_tasks(request_body, task_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id FROM cloudcomputingtask.tbl_users WHERE user_email = ?', request_body['user_email'])
        user_id = int(cursor.fetchall())

        cursor.execute('DELETE FROM cloudcomputingtask.tbl_tasks WHERE user_id = ? AND task_id = ?', (user_id, task_id))
        conn.commit()
        conn.close()
    return 0
