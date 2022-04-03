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
        user_exists = cursor.execute ('SELECT user_md5_pass FROM cloudcomputingtask.tbl_users WHERE user_email = ?', user_email)
        if user_exists == 0:
            session_key = "401, Incorrect email provided"

        else:
            md5Pass_db = str(cursor.fetchall())
            if md5Pass_db == hashlib.md5(user_password.encode('utf-8')):
                session_key = hashlib.md5(secrets.token_urlsafe(10).encode('utf-8'))
                cursor.execute('INSERT INTO cloudcomputingtask.tbl_users (user_api_key) VALUES(%s)', (session_key))
            else:
                session_key = "401, Incorrect password"
    conn.close()
    return session_key



def auth (user_api_key):
    conn = open_connection()
    with conn.cursor() as cursor:
        user_exists = cursor.execute ('SELECT * FROM cloudcomputingtask.tbl_users WHERE user_api_key = ?', user_api_key)
    conn.close()
    if user_exists == 0:
        return False

    else:
        return True
