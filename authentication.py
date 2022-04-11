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
    conn = pymysql.connect(user="cloudcomputing", password='cloudcomputing', db=db_name, host='35.246.95.43', cursorclass=pymysql.cursors.DictCursor)
    return conn

# Authentication
def login (user_email, user_password):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_users WHERE user_email = %s', user_email)
        db_row = cursor.fetchall()
        user_exists = cursor.rowcount
        if user_exists < 1:
            session_key = "401, Incorrect email provided"

        else:
            if db_row[0]['user_md5_pass'] == hashlib.md5(user_password.encode('utf-8')).hexdigest():
                session_key = hashlib.md5(secrets.token_urlsafe(10).encode('utf-8')).hexdigest()
                username = db_row[0]['username']
                cursor.execute('UPDATE cloudcomputingtask.tbl_users SET user_api_key = %s WHERE username = %s', (session_key, username))
            else:
                session_key = "401, Incorrect password"
    conn.commit()
    conn.close()
    return session_key



def auth (user_api_key):
    conn = open_connection()
    with conn.cursor() as cursor:
        user_exists = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_users WHERE user_api_key = %s', user_api_key)
    conn.close()
    if user_exists == 0:
        return False

    else:
        return True

# function to check for admin priviledges 
def admin(user_api_key):
    conn = open_connection()
    with conn.cursor() as cursor:
        is_admin = cursor.execute('SELECT * FROM cloudcomputingtask.tbl_users WHERE user_api_key = %s AND role = %s', (user_api_key, "admin"))
    conn.close()
    if is_admin == 0:
        return False
    else:
        return True
    
