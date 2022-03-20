import os
import pymysql
from flask import jsonify, request
import secrets
import hashlib

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


'''Tasks CRUD'''

# READ function to see all tasks
def get_user_tasks(request_body):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id FROM cloudcomputingtask.tbl_users WHERE user_email = ?', request_body['user_email'])
        user_id = int(cursor.fetchall())

        if task_id == 0:
            result = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_tasks WHERE user_id = ?', user_id)
            tasks = cursor.fetchall()
            if result > 0:
                answer = jsonify(tasks)
            else:
                answer = 'No Active Tasks Found'

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

        cursor.execute('INSERT INTO cloudcomputingtask.tbl_tasks (task_id, user_id, user_api_key, task_title, task_description, task_status, task_created_datetime, task_updated_datetime) VALUES(%s,%s, %s, %s,%s, %s, NOW(), NOW())',
        (secrets.token_urlsafe(5), user_id, request_body['user_api_key'], request_body["task_title"], request_body["task_description"], request_body["task_status"]))
        conn.commit()
        conn.close()
    return 0


def update_user_tasks(request_body):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id FROM cloudcomputingtask.tbl_users WHERE user_email = ?', request_body['user_email'])
        user_id = int(cursor.fetchall())

        if "task_title" in request_body:
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_title = ?, task_updated_datetime = NOW() WHERE user_id = ?', (request_body['task_title'], user_id))

        if "task_description" in request_body:
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_description = ?, task_updated_datetime = NOW() WHERE user_id = ?', (request_body['task_description'], user_id))

        if "task_status" in request_body:
            cursor.execute('UPDATE cloudcomputingtask.tbl_tasks SET task_status = ?, task_updated_datetime = NOW() WHERE user_id = ?', (request_body['task_status'], user_id))
        conn.commit()
        conn.close()
    return 0


def delete_user_tasks(request_body):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id FROM cloudcomputingtask.tbl_users WHERE user_email = ?', request_body['user_email'])
        user_id = int(cursor.fetchall())

        cursor.execute('DELETE FROM cloudcomputingtask.tbl_tasks WHERE user_id = ? AND task_id = ?', (user_id, request_body['task_id']))
        conn.commit()
        conn.close()
    return 0
